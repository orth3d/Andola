import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','AnDjo.settings')

import django
django.setup()

# Fake population script

import random
from usuariosAnd.models import Usuario
from faker import Faker

fakegen = Faker()

def populate(N=5):

    for entry in range(N):
        fake_nombre = fakegen.first_name()
        fake_apellido = fakegen.last_name()
        fake_fecha_nacimiento = fakegen.date()
        fake_telefono = fakegen.phone_number()
        fake_mail = fakegen.company_email()
        fake_rfc = fakegen.ssn()

    # create data entry

        Usuario.objects.get_or_create(nombre=fake_nombre,apellido=fake_apellido,fecha_nacimiento=fake_fecha_nacimiento,telefono=fake_telefono,mail=fake_mail,rfc=fake_rfc)[0]
        # fakeUsr = Usuario.objects.get_or_create(nombre=fake_nombre,apellido=fake_apellido,fecha_nacimiento=fake_fecha_nacimiento,telefono=fake_telefono,mail=fake_mail,rfc=fake_rfc)[0]

if __name__ == '__main__':
    print("Populating script")
    populate(20)
    print("Populating Complete")