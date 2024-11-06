from ms_core import BaseCRUD

from app.models import User
from app.schemas import UserSchema

class UserCRUD(BaseCRUD[User, UserSchema]):
    model = User
    schema = UserSchema
