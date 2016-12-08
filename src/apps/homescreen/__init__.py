from trezor.wire import register, protobuf_workflow
from trezor.utils import unimport
from trezor.messages.wire_types import Initialize, GetFeatures, Ping


async def respond_Features(session_id, msg):
    from ..common import storage, coins
    from trezor.messages.Features import Features

    f = Features()
    f.vendor = 'bitcointrezor.com'
    f.revision = '0123456789'
    f.bootloader_hash = '0123456789'
    f.major_version = 2
    f.minor_version = 0
    f.patch_version = 0
    f.coins = coins.COINS

    f.device_id = storage.get_device_id()
    f.label = storage.get_label()
    f.initialized = storage.is_initialized()
    f.pin_protection = storage.is_protected_by_pin()
    f.passphrase_protection = storage.is_protected_by_passphrase()

    return f


async def respond_Pong(session_id, msg):
    from trezor.messages.Success import Success
    s = Success()
    s.message = msg.message
    # TODO: handle other fields:
    # button_protection
    # passphrase_protection
    # pin_protection
    return s


def boot():
    register(Initialize, protobuf_workflow, respond_Features)
    register(GetFeatures, protobuf_workflow, respond_Features)
    register(Ping, protobuf_workflow, respond_Pong)
