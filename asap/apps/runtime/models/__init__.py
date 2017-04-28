"""
Each VRT will get a unique access token and identifier
which will be used for obtaining `Widgets`.

Currently there are 2 types of VRTs:
 - Badge
 - Terminal

### User Application:

 - The User will authenticate itself using the Password Grant Flow (OAuth2)
    and receive an access token for further communication.
 - The access token will be used for obtaining the membership information.
    Each membership information may have multiple VRTs associated with it.
 - Each VRT will obtain its widgets using its identifier and the access token.
    (Access Token used by VRT may be different from the user's access token,
    and is an implementation detail which might change)


### Direct VRT (Terminal)
 - The VRT will get the access token and unique identifier directly. (Maybe with these embedded in QR for now).

"""
from . import runtime
from . import runtime_locker
from . import session

from .. import signals