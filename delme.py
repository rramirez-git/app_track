from app_cliente.models import Cliente, TaxonomiaExpediente
from app_cliente.cliente.models import UserProfilePkCliente, UserProfilePkNoCliente, UserProfileResponsables
from zend_django.models import UserProfile
from django.contrib.auth.models import User
from random import randint

def f1():
    txexp = TaxonomiaExpediente.objects.get_or_create(nombre=f"TE_{randint(0,100)}")[0]
    strusr = f"usuario_{randint(0,10000)}"
    usrs = list()
    numregs = 3
    for x in range(numregs):
        strusr = f"usuario_{randint(0,10000)}"
        usrs.append(User.objects.get_or_create(
            username= strusr,
            email=f"{strusr}@mail.com",
            password=strusr,
            first_name=strusr,
            last_name=strusr,
        )[0])
    usrps = list()
    for x in range(numregs - 1):
        usrps.append(UserProfile.objects.get_or_create(
            user=usrs[x],
            apellido_materno=usrs[x].first_name,
            telefono=f"{randint(1000,9999)}"
        )[0])
    ctes = list()
    for x in range(numregs - 2):
        ctes.append(Cliente.objects.get_or_create(
            userprofile=usrps[x], 
            tipo=txexp
        )[0])
    print(txexp, usrs, usrps, ctes)
    print(UserProfilePkCliente())
    print(UserProfilePkNoCliente())
    print(UserProfileResponsables())

f1()