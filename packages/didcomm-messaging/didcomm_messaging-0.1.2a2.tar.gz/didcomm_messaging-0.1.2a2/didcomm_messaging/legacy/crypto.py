"""DIDComm v1 packing and unpacking.

This implementation is kept around for backwards compatibility. It is
likely that you should use the V1CryptoService interfaces instead.
"""

from collections import OrderedDict
from typing import Iterable, Optional, Sequence, Dict, Union, Tuple, cast
import json
import struct
import time

import base58

try:
    import msgpack
    import nacl.bindings
    import nacl.exceptions
    import nacl.utils
except ImportError as err:
    raise ImportError(
        "V1 implementation requires 'legacy' extra to be installed"
    ) from err

from didcomm_messaging.multiformats.multibase import Base64UrlEncoder


class CryptoError(Exception):
    """CryptoError raised on failed crypto call."""


b64url = Base64UrlEncoder()


def b64_to_bytes(val: str) -> bytes:
    """Convert a base 64 string to bytes."""
    return b64url.decode(val)


def bytes_to_b64(val: bytes) -> str:
    """Convert a byte string to base 64."""
    return b64url.encode(val)


def b58_to_bytes(val: str) -> bytes:
    """Convert a base 58 string to bytes.

    Small cache provided for key conversions which happen frequently in pack
    and unpack and message handling.
    """
    return base58.b58decode(val)


def bytes_to_b58(val: bytes) -> str:
    """Convert a byte string to base 58.

    Small cache provided for key conversions which happen frequently in pack
    and unpack and message handling.
    """
    return base58.b58encode(val).decode()


def create_keypair(seed: Union[str, bytes, None] = None) -> Tuple[bytes, bytes]:
    """Create a public and private signing keypair from a seed value.

    Args:
        seed: Seed for keypair

    Returns:
        A tuple of (public key, secret key)

    """
    if seed:
        seed = validate_seed(seed)
    else:
        seed = random_seed()
    pk, sk = nacl.bindings.crypto_sign_seed_keypair(seed)
    return pk, sk


def random_seed() -> bytes:
    """Generate a random seed value.

    Returns:
        A new random seed

    """
    return nacl.utils.random(nacl.bindings.crypto_secretbox_KEYBYTES)


def validate_seed(seed: Union[str, bytes]) -> bytes:
    """Convert a seed parameter to standard format and check length.

    Args:
        seed: The seed to validate

    Returns:
        The validated and encoded seed

    """
    if isinstance(seed, str):
        if "=" in seed:
            seed = b64_to_bytes(seed)
        else:
            seed = seed.encode()
    if not isinstance(seed, bytes):
        raise CryptoError("Seed value is not a string or bytes")
    if len(seed) != 32:
        raise CryptoError("Seed value must be 32 bytes in length")
    return seed


def sign_message(message: bytes, secret: bytes) -> bytes:
    """Sign a message using a private signing key.

    Args:
        message: The message to sign
        secret: The private signing key

    Returns:
        The signature

    """
    result = nacl.bindings.crypto_sign(message, secret)
    sig = result[: nacl.bindings.crypto_sign_BYTES]
    return sig


def verify_signed_message(signed: bytes, verkey: bytes) -> bool:
    """Verify a signed message according to a public verification key.

    Args:
        signed: The signed message
        verkey: The verkey to use in verification

    Returns:
        True if verified, else False

    """
    try:
        nacl.bindings.crypto_sign_open(signed, verkey)
    except nacl.exceptions.BadSignatureError:
        return False
    return True


def sign_message_field(field_value: Dict, signer: str, secret: bytes) -> Dict:
    """Sign a field of a message and return the value of a signature decorator."""
    timestamp_bytes = struct.pack(">Q", int(time.time()))
    sig_data_bytes = timestamp_bytes + json.dumps(field_value).encode()
    sig_data = bytes_to_b64(
        sig_data_bytes,
    )

    signature_bytes = nacl.bindings.crypto_sign(sig_data_bytes, secret)[
        : nacl.bindings.crypto_sign_BYTES
    ]
    signature = bytes_to_b64(
        signature_bytes,
    )

    return {
        "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec"
        "/signature/1.0/ed25519Sha512_single",
        "signer": signer,
        "sig_data": sig_data,
        "signature": signature,
    }


def verify_signed_message_field(signed_field: Dict) -> Tuple[str, Dict]:
    """Verify a signed message field."""
    data_bytes = b64_to_bytes(
        signed_field["sig_data"],
    )
    signature_bytes = b64_to_bytes(
        signed_field["signature"],
    )
    nacl.bindings.crypto_sign_open(
        signature_bytes + data_bytes, b58_to_bytes(signed_field["signer"])
    )

    fieldjson = data_bytes[8:]
    return signed_field["signer"], json.loads(fieldjson)


def anon_crypt_message(message: bytes, to_verkey: bytes) -> bytes:
    """Apply anon_crypt to a binary message.

    Args:
        message: The message to encrypt
        to_verkey: The verkey to encrypt the message for

    Returns:
        The anon encrypted message

    """
    pk = nacl.bindings.crypto_sign_ed25519_pk_to_curve25519(to_verkey)
    enc_message = nacl.bindings.crypto_box_seal(message, pk)
    return enc_message


def anon_decrypt_message(enc_message: bytes, secret: bytes) -> bytes:
    """Apply anon_decrypt to a binary message.

    Args:
        enc_message: The encrypted message
        secret: The seed to use

    Returns:
        The decrypted message

    """
    sign_pk, sign_sk = create_keypair(secret)
    pk = nacl.bindings.crypto_sign_ed25519_pk_to_curve25519(sign_pk)
    sk = nacl.bindings.crypto_sign_ed25519_sk_to_curve25519(sign_sk)

    message = nacl.bindings.crypto_box_seal_open(enc_message, pk, sk)
    return message


def auth_crypt_message(
    message: bytes, to_verkey: bytes, from_verkey: bytes, from_sigkey: bytes
) -> bytes:
    """Apply auth_crypt to a binary message.

    Args:
        message: The message to encrypt
        to_verkey: To recipient's verkey
        from_verkey: Sender verkey, included in combo box for verification
        from_sigkey: Sender sigkey, included to auth encrypt the message

    Returns:
        The encrypted message

    """
    nonce = nacl.utils.random(nacl.bindings.crypto_box_NONCEBYTES)
    target_pk = nacl.bindings.crypto_sign_ed25519_pk_to_curve25519(to_verkey)
    sk = nacl.bindings.crypto_sign_ed25519_sk_to_curve25519(from_sigkey)
    enc_body = nacl.bindings.crypto_box(message, nonce, target_pk, sk)
    combo_box = OrderedDict(
        [
            ("msg", bytes_to_b64(enc_body)),
            ("sender", bytes_to_b58(from_verkey)),
            ("nonce", bytes_to_b64(nonce)),
        ]
    )
    combo_box_bin = cast(bytes, msgpack.packb(combo_box, use_bin_type=True))
    enc_message = nacl.bindings.crypto_box_seal(combo_box_bin, target_pk)
    return enc_message


def auth_decrypt_message(
    enc_message: bytes, my_verkey: bytes, my_sigkey: bytes
) -> Tuple[bytes, str]:
    """Apply auth_decrypt to a binary message.

    Args:
        enc_message: The encrypted message
        my_verkey: Public key for signing keys
        my_sigkey: Secret key for decrypting for signing key

    Returns:
        A tuple of (decrypted message, sender verkey)

    """
    pk = nacl.bindings.crypto_sign_ed25519_pk_to_curve25519(my_verkey)
    sk = nacl.bindings.crypto_sign_ed25519_sk_to_curve25519(my_sigkey)
    body = nacl.bindings.crypto_box_seal_open(enc_message, pk, sk)

    unpacked = msgpack.unpackb(body, raw=False)
    sender_vk = unpacked["sender"]
    nonce = b64_to_bytes(unpacked["nonce"])
    enc_message = b64_to_bytes(unpacked["msg"])
    sender_pk = nacl.bindings.crypto_sign_ed25519_pk_to_curve25519(
        b58_to_bytes(sender_vk)
    )
    message = nacl.bindings.crypto_box_open(enc_message, nonce, sender_pk, sk)
    return message, sender_vk


def prepare_pack_recipient_keys(
    to_verkeys: Sequence[bytes],
    from_verkey: Optional[bytes] = None,
    from_sigkey: Optional[bytes] = None,
) -> Tuple[str, bytes]:
    """Assemble the recipients block of a packed message.

    Args:
        to_verkeys: Verkeys of recipients
        from_verkey: Sender Verkey needed to authcrypt package
        from_sigkey: Sender Sigkey needed to authcrypt package

    Returns:
        A tuple of (json result, key)

    """
    if (
        from_verkey is not None
        and from_sigkey is None
        or from_sigkey is not None
        and from_verkey is None
    ):
        raise CryptoError(
            "Both verkey and sigkey needed to authenticated encrypt message"
        )

    cek = nacl.bindings.crypto_secretstream_xchacha20poly1305_keygen()
    recips = []

    for target_vk in to_verkeys:
        target_pk = nacl.bindings.crypto_sign_ed25519_pk_to_curve25519(target_vk)
        if from_verkey and from_sigkey:
            sender_vk = bytes_to_b58(from_verkey).encode()
            enc_sender = nacl.bindings.crypto_box_seal(sender_vk, target_pk)
            sk = nacl.bindings.crypto_sign_ed25519_sk_to_curve25519(from_sigkey)

            nonce = nacl.utils.random(nacl.bindings.crypto_box_NONCEBYTES)
            enc_cek = nacl.bindings.crypto_box(cek, nonce, target_pk, sk)
        else:
            enc_sender = None
            nonce = None
            enc_cek = nacl.bindings.crypto_box_seal(cek, target_pk)

        recips.append(
            OrderedDict(
                [
                    (
                        "encrypted_key",
                        bytes_to_b64(
                            enc_cek,
                        ),
                    ),
                    (
                        "header",
                        OrderedDict(
                            [
                                ("kid", bytes_to_b58(target_vk)),
                                (
                                    "sender",
                                    bytes_to_b64(
                                        enc_sender,
                                    )
                                    if enc_sender
                                    else None,
                                ),
                                (
                                    "iv",
                                    bytes_to_b64(
                                        nonce,
                                    )
                                    if nonce
                                    else None,
                                ),
                            ]
                        ),
                    ),
                ]
            )
        )

    data = OrderedDict(
        [
            ("enc", "xchacha20poly1305_ietf"),
            ("typ", "JWM/1.0"),
            ("alg", "Authcrypt" if from_verkey else "Anoncrypt"),
            ("recipients", recips),
        ]
    )
    return json.dumps(data), cek


def locate_pack_recipient_key(
    recipients: Sequence[dict], my_verkey: bytes, my_sigkey: bytes
) -> Tuple[bytes, Optional[str], str]:
    """Locate pack recipient key.

    Decode the encryption key and sender verification key from a
    corresponding recipient block, if any is defined.

    Args:
        recipients: Recipients to locate
        my_verkey: verkey to use
        my_sigkey: sigkey to use

    Returns:
        A tuple of (cek, sender_vk, recip_vk_b58)

    Raises:
        ValueError: If no corresponding recipient key found

    """
    not_found = []
    for recip in recipients:
        if not recip or "header" not in recip or "encrypted_key" not in recip:
            raise ValueError("Invalid recipient header")

        recip_vk_b58 = recip["header"].get("kid")

        if bytes_to_b58(my_verkey) != recip_vk_b58:
            not_found.append(recip_vk_b58)
            continue

        pk = nacl.bindings.crypto_sign_ed25519_pk_to_curve25519(my_verkey)
        sk = nacl.bindings.crypto_sign_ed25519_sk_to_curve25519(my_sigkey)

        encrypted_key = b64_to_bytes(
            recip["encrypted_key"],
        )

        if (
            "iv" in recip["header"]
            and recip["header"]["iv"]
            and "sender" in recip["header"]
            and recip["header"]["sender"]
        ):
            nonce: Optional[bytes] = b64_to_bytes(
                recip["header"]["iv"],
            )
            enc_sender: Optional[bytes] = b64_to_bytes(
                recip["header"]["sender"],
            )

        else:
            nonce = None
            enc_sender = None

        if nonce and enc_sender:
            sender_vk = nacl.bindings.crypto_box_seal_open(enc_sender, pk, sk).decode()
            sender_pk = nacl.bindings.crypto_sign_ed25519_pk_to_curve25519(
                b58_to_bytes(sender_vk)
            )
            cek = nacl.bindings.crypto_box_open(encrypted_key, nonce, sender_pk, sk)
        else:
            sender_vk = None
            cek = nacl.bindings.crypto_box_seal_open(encrypted_key, pk, sk)
        return cek, sender_vk, recip_vk_b58
    raise ValueError(
        "Verkey {} not found in {}".format(bytes_to_b58(my_verkey), not_found)
    )


def encrypt_plaintext(
    message: str, add_data: bytes, key: bytes
) -> Tuple[bytes, bytes, bytes]:
    """Encrypt the payload of a packed message.

    Args:
        message: Message to encrypt
        add_data: additional data
        key: Key used for encryption

    Returns:
        A tuple of (ciphertext, nonce, tag)

    """
    nonce = nacl.utils.random(nacl.bindings.crypto_aead_chacha20poly1305_ietf_NPUBBYTES)
    message_bin = message.encode()
    output = nacl.bindings.crypto_aead_chacha20poly1305_ietf_encrypt(
        message_bin, add_data, nonce, key
    )
    mlen = len(message)
    ciphertext = output[:mlen]
    tag = output[mlen:]
    return ciphertext, nonce, tag


def decrypt_plaintext(
    ciphertext: bytes, recips_bin: bytes, nonce: bytes, key: bytes
) -> str:
    """Decrypt the payload of a packed message.

    Returns:
        The decrypted string

    """
    output = nacl.bindings.crypto_aead_chacha20poly1305_ietf_decrypt(
        ciphertext, recips_bin, nonce, key
    )
    return output.decode()


def pack_message(
    message: str,
    to_verkeys: Sequence[bytes],
    from_verkey: Optional[bytes] = None,
    from_sigkey: Optional[bytes] = None,
) -> OrderedDict:
    """Assemble a packed message for a set of recipients, optionally including the sender.

    Args:
        message: The message to pack
        to_verkeys: The verkeys to pack the message for
        from_verkey: The sender verkey
        from_sigkey: The sender sigkey

    Returns:
        The encoded message

    """
    recips_json, cek = prepare_pack_recipient_keys(to_verkeys, from_verkey, from_sigkey)
    recips_b64 = bytes_to_b64(
        recips_json.encode(),
    )

    ciphertext, nonce, tag = encrypt_plaintext(message, recips_b64.encode(), cek)

    data = OrderedDict(
        [
            ("protected", recips_b64),
            (
                "iv",
                bytes_to_b64(
                    nonce,
                ),
            ),
            (
                "ciphertext",
                bytes_to_b64(
                    ciphertext,
                ),
            ),
            (
                "tag",
                bytes_to_b64(
                    tag,
                ),
            ),
        ]
    )
    return data


def recipients_from_packed_message(message_bytes: bytes) -> Iterable[str]:
    """Inspect the header of the packed message and extract the recipient key."""
    try:
        wrapper = json.loads(message_bytes)
    except Exception as error:
        raise ValueError("Invalid packed message") from error

    recips_json = b64_to_bytes(
        wrapper["protected"],
    ).decode()

    try:
        recips_outer = json.loads(recips_json)
    except Exception as error:
        raise ValueError("Invalid packed message recipients") from error

    return [recip["header"]["kid"] for recip in recips_outer["recipients"]]


def unpack_message(
    enc_message: Union[Dict, bytes], my_verkey: bytes, my_sigkey: bytes
) -> Tuple[str, Optional[str], str]:
    """Decode a packed message.

    Disassemble and unencrypt a packed message, returning the message content,
    verification key of the sender (if available), and verification key of the
    recipient.

    Args:
        enc_message: The encrypted message
        my_verkey: verkey to use
        my_sigkey: sigkey to use

    Returns:
        A tuple of (message, sender_vk, recip_vk)

    Raises:
        ValueError: If the packed message is invalid
        ValueError: If the packed message reipients are invalid
        ValueError: If the pack algorithm is unsupported
        ValueError: If the sender's public key was not provided

    """
    if isinstance(enc_message, bytes):
        try:
            enc_message = json.loads(enc_message)
        except Exception as err:
            raise ValueError("Invalid packed message") from err
    if not isinstance(enc_message, dict):
        raise TypeError("Expected bytes or dict, got {}".format(type(enc_message)))

    protected_bin = enc_message["protected"].encode()
    recips_json = b64_to_bytes(
        enc_message["protected"],
    ).decode()
    try:
        recips_outer = json.loads(recips_json)
    except Exception as err:
        raise ValueError("Invalid packed message recipients") from err

    alg = recips_outer["alg"]
    is_authcrypt = alg == "Authcrypt"
    if not is_authcrypt and alg != "Anoncrypt":
        raise ValueError("Unsupported pack algorithm: {}".format(alg))
    cek, sender_vk, recip_vk = locate_pack_recipient_key(
        recips_outer["recipients"], my_verkey, my_sigkey
    )
    if not sender_vk and is_authcrypt:
        raise ValueError("Sender public key not provided for Authcrypt message")

    ciphertext = b64_to_bytes(
        enc_message["ciphertext"],
    )
    nonce = b64_to_bytes(
        enc_message["iv"],
    )
    tag = b64_to_bytes(
        enc_message["tag"],
    )

    payload_bin = ciphertext + tag
    message = decrypt_plaintext(payload_bin, protected_bin, nonce, cek)

    return message, sender_vk, recip_vk
