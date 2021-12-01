class PetUrlSwitcher:
    switcher = {
        'dog': 'Собака',
        'cat': 'Кошка'
    }

    @staticmethod
    def switch(pet):
        return PetUrlSwitcher.switcher.get(pet, None)
