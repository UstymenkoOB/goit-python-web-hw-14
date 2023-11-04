from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field


class ContactBase(BaseModel):
    """
    Base model for a contact. Contains common contact information.

    :param name: The name of the contact.
    :type name: str
    :param surname: The surname of the contact.
    :type surname: str
    :param email: The email address of the contact.
    :type email: str
    :param phone: The phone number of the contact.
    :type phone: str
    :param birthday: The birthday of the contact.
    :type birthday: date
    """
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: str = Field(max_length=100)
    phone: str = Field(max_length=15)
    birthday: date


class ContactModel(ContactBase):
    """
    Model for creating a contact. Extends ContactBase and adds a description.

    :param description: The description of the contact.
    :type description: str
    """
    description: str = Field(max_length=150)


class ContactUpdate(ContactModel):
    """
    Model for updating a contact. Inherits from ContactModel, allowing updates.

    The ContactUpdate model inherits all fields from ContactModel.

    Additional fields can be updated as needed.
    """
    ...


class ContactResponse(ContactBase):
    """
    Model for a contact response. Extends ContactBase and includes an 'id' field.

    :param id: The unique identifier of the contact.
    :type id: int
    """
    id: int
    
    class Config:
        from_attributes = True


class UserModel(BaseModel):
    """
    Model for a user. Contains user information for registration.

    :param username: The username of the user.
    :type username: str
    :param email: The email address of the user.
    :type email: str
    :param password: The user's password.
    :type password: str
    """
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    """
    Model for user data in the database. Extends BaseModel and includes additional user data.

    :param id: The unique identifier of the user.
    :type id: int
    :param username: The username of the user.
    :type username: str
    :param email: The email address of the user.
    :type email: str
    :param created_at: The date and time when the user account was created.
    :type created_at: datetime
    :param avatar: The URL to the user's avatar.
    :type avatar: str
    """
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """
    Model for a user response. Contains user data and a detail message.

    :param user: The user's data.
    :type user: UserDb
    :param detail: A message indicating the success of a user-related operation.
    :type detail: str
    """
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    """
    Model for an authentication token.

    :param access_token: The access token.
    :type access_token: str
    :param refresh_token: The refresh token.
    :type refresh_token: str
    :param token_type: The token type (default is "bearer").
    :type token_type: str
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    """
    Model for requesting email-related operations.

    :param email: The email address for email-related operations.
    :type email: EmailStr
    """
    email: EmailStr
