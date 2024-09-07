from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class SendPaidReaction(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``186``
        - ID: ``25C8FE3E``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        msg_id (``int`` ``32-bit``):
            N/A

        count (``int`` ``32-bit``):
            N/A

        random_id (``int`` ``64-bit``):
            N/A

        private (``bool``, *optional*):
            N/A

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["peer", "msg_id", "count", "random_id", "private"]

    ID = 0x25c8fe3e
    QUALNAME = "functions.messages.SendPaidReaction"

    def __init__(self, *, peer: "raw.base.InputPeer", msg_id: int, count: int, random_id: int, private: Optional[bool] = None) -> None:
        self.peer = peer  # InputPeer
        self.msg_id = msg_id  # int
        self.count = count  # int
        self.random_id = random_id  # long
        self.private = private  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendPaidReaction":
        
        flags = Int.read(b)
        
        private = True if flags & (1 << 0) else False
        peer = TLObject.read(b)
        
        msg_id = Int.read(b)
        
        count = Int.read(b)
        
        random_id = Long.read(b)
        
        return SendPaidReaction(peer=peer, msg_id=msg_id, count=count, random_id=random_id, private=private)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.private else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(Int(self.msg_id))
        
        b.write(Int(self.count))
        
        b.write(Long(self.random_id))
        
        return b.getvalue()
