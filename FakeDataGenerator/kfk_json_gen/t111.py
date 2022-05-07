from mimesis import Person,Food
from mimesis.locales import LIST_OF_LOCALES

class User(object):
    """
    User record

    Args:
        name (str): User's name

        favorite_number (int): User's favorite number

        favorite_color (str): User's favorite color

        address(str): User's address; confidential

    """
    def __init__(self, name, address, favorite_number, favorite_color):
        self.name = name
        self.favorite_number = favorite_number
        self.favorite_color = favorite_color
        # address should not be serialized, see user_to_dict()
        self._address = address

class gen_data:
    def __init__(self):
        pass

    def gen_name(self):
        return Person().name()



def user_to_dict(user, ctx):
    """
    Returns a dict representation of a User instance for serialization.

    Args:
        user (User): User instance.

        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.

    Returns:
        dict: Dict populated with user attributes to be serialized.

    """
    # User._address must not be serialized; omit from dict
    return dict(name=user.name,
                favorite_number=user.favorite_number,
                favorite_color=user.favorite_color)


# while True:
    # # Serve on_delivery callbacks from previous calls to produce()
    # try:
    #     user_name = input("Enter name: ")
    #     user_address = input("Enter address: ")
    #     user_favorite_number = int(input("Enter favorite number: "))
    #     user_favorite_color = input("Enter favorite color: ")
    #     user = User(name=user_name,
    #                 address=user_address,
    #                 favorite_color=user_favorite_color,
    #                 favorite_number=user_favorite_number)
    #     producer.produce(topic=topic, key=str(uuid4()), value=user,
    #                      on_delivery=delivery_report)
    # except KeyboardInterrupt:
    #     break
    # except ValueError:
    #     print("Invalid input, discarding record...")
    #     continue

g1 = gen_data()

fu1 = Food().fruit()
# print(g1.gen_name())
print(fu1)