from datetime import datetime
import re
from turtle import update  # case sensivity için kullanılacak
# global variables
# Kayıtlı kullanıcılar buraya eklenebilir
users = {
    "ahmet": "İstinye123",
    "meryem": "4444",
}

shoppingCart = {}

# Envanter => envanter adı [stok adedi, fiyatı]
inventory = {"kuskonmaz": [6, 3], "brokoli": [20, 7], "havuç": [15, 5], "elmalar": [25, 15], "muz":
             [19, 18], "meyve": [23, 5], "yumurta": [44, 4], "karısık meyve suyu": [1, 19], "balık çubukları":
             [27, 10], "dondurma": [0, 4], "elma suyu": [33, 8], "portakal suyu": [32, 4], "üzüm suyu":
             [21, 16]}

# functions
# Menü bilgilerinin gösterildiği alan.


def login():
    print("**** Istinye Online Market'e Hosgeldiniz ****")
    print("Lütfen kullanıcı kimlik bilgilerinizi saglayarak giris yapın:")
    userName = input("Kullanıcı adı: ")
    passWord = input("Şifre: ")
    while(users.get(userName) == None or users.get(userName) != passWord):
        print("Kullanıcı adınız ve / veya sifreniz dogru degil. Lütfen tekrar deneyin!")
        userName = input("Kullanıcı adı: ")
        passWord = input("Şifre: ")

    print("Basarıyla giris yapıldı!")
    print("Hosgeldiniz {}! Lütfen ilgili menü numarasını girerek asagıdaki seçeneklerden birini seçin.".format(userName))


def searchProduct():
    productKeyword = input("Ne arıyorsunuz? ")
    searchedProductList = []
    # aranacak anahtar kelime ile filtrelenecek yeni listenin bulunması
    # ör: suyu yazınca sadece suyu key'i içeren dict. elemanlarının listelenmesi
    # inventory[key][0] > 0 ile de stok sayısı 0'dan büyük olanlar listelenecektir.
    for key in inventory.keys():
        if re.search(productKeyword, key, re.IGNORECASE) and inventory[key][0] > 0:
            searchedProductList.append(key)

    # Sorgulama sonucunda listenin boş olması durumu
    while len(searchedProductList) <= 0:
        productKeyword = input(
            "Aramanız hiçbir ögeyle eslesmedi. Lütfen baska bir sey deneyin (Ana menü için 0 girin): ")
        if productKeyword == "0":
            return
        else:
            for key in inventory.keys():
                if re.search(productKeyword, key, re.IGNORECASE) and inventory[key][0] > 0:
                    searchedProductList.append(key)

    print("{} benzer ürün bulundu".format(len(searchedProductList)))

    # indexi searchedProductList üzerinden de bulabilirdik ama ekstra iterasyon zaman alacağından bu şekilde de işler.
    i = 1
    for searchedProduct in searchedProductList:
        print("{}. {} {} $".format(
            i, searchedProduct, inventory[searchedProduct][1]))
        i += 1

    productChoice = int(input(
        "Lütfen sepetinize eklemek istediginiz ürünü seçin (Ana menü için 0 girin): "))

    # Ürün miktarı seçildikten sonrası
    while productChoice != 0:
        if productChoice > len(searchedProductList) or productChoice < 0:
            print("Geçerli bir seçim yapınız.")
            productChoice = int(input(
                "Lütfen sepetinize eklemek istediginiz ürünü seçin (Ana menü için 0 girin): "))
            continue

        addedProductKey = searchedProductList[productChoice-1]
        amount = int(
            input("{} ekleniyor. Tutarı Girin: ".format(addedProductKey)))
        if(amount > inventory[addedProductKey][0]):
            print(
                "Üzgünüm! Miktar sınırı asıyor, Lütfen daha küçük bir miktarla tekrar deneyin")
        else:
            price = inventory[addedProductKey][1]
            shoppingCart[addedProductKey] = [amount, price * amount]
            print("Sepetinize {} eklendi.\nAna menüye geri dönülüyor".format(
                addedProductKey))
            return

        productChoice = int(input(
            "Lütfen sepetinize eklemek istediginiz ürünü seçin (Ana menü için 0 girin): "))


def printBars():
    print("_______________________________")


def goToCart():
    print("Sepetiniz artık sunları içeriyor: ")
    if len(shoppingCart) == 0:
        print("Sepetiniz boş.\ntoplam: 0 $")
    else:
        cartSubMenuChoice = 0
        while cartSubMenuChoice != 4:
            totalCost = 0
            i = 1
            for shoppingItemKey in shoppingCart.keys():
                print("{}. {} fiyatı = {} $ miktar = {} toplam = {}$".format(i, shoppingItemKey, inventory[shoppingItemKey][1],
                                                                             shoppingCart[shoppingItemKey][0], shoppingCart[shoppingItemKey][1]))
                totalCost += shoppingCart[shoppingItemKey][1]
                i += 1

            print("Toplam: {} $".format(totalCost))
            printCartMenu()
            cartSubMenuChoice = int(input("Seçiminiz: "))
            match(cartSubMenuChoice):
                case 1:  # Tutarı güncelleyin
                    updateItemIndex = int(input(
                        "Lütfen miktarını değiştireceğiniz ögeyi seçin: "))
                    if len(shoppingCart.keys()) < updateItemIndex or updateItemIndex <= 0:
                        print("Siparişte bulunmayan bir seçim yaptınız.")
                        break

                    amount = int(input("Lütfen yeni miktarı yazın: "))

                    i = 1
                    for shoppingCartKey in shoppingCart.keys():
                        if i == updateItemIndex:
                            keyUpdated = shoppingCartKey
                            break
                        i += 1

                    if inventory[keyUpdated][0] < amount:
                        print(
                            "Üzgünüm! Miktar sınırı asıyor, Lütfen daha küçük bir miktarla tekrar deneyin")
                    else:
                        shoppingCart[keyUpdated][0] = amount
                        shoppingCart[keyUpdated][1] = amount * \
                            inventory[keyUpdated][1]
                    break
                case 2:  # Bir ögeyi kaldırın
                    removeItemIndex = int(
                        input("Kaldırmak istediğiniz ürün: "))

                    if len(shoppingCart.keys()) < removeItemIndex or removeItemIndex <= 0:
                        print("Siparişte bulunmayan bir seçim yaptınız.")
                        break

                    i = 1
                    for shoppingCartKey in shoppingCart.keys():
                        if i == removeItemIndex:
                            keyRemoved = shoppingCartKey
                            break
                        i += 1

                    del shoppingCart[keyRemoved]
                    break
                case 3:  # Satın al
                    purchase()
                case 4:
                    break
                case _:
                    print("Geçerli bir seçim yapınız.")


def purchase():
    totalCost = 0
    # makbuzun işlenmesi ve listedeki ürünlerin yansıtılması
    print("Makbuzunuz isleniyor ...")
    print("*******************************")
    print("\t 0850 283 6000\n\t istinye.edu.tr")
    printBars()
    for shoppingItemKey in shoppingCart.keys():
        print("{} {} $ miktar = {} toplam = {} $".format(shoppingItemKey, inventory[shoppingItemKey][1],
                                                         shoppingCart[shoppingItemKey][0], shoppingCart[shoppingItemKey][1]))
        totalCost += shoppingCart[shoppingItemKey][1]
    printBars()
    print("Toplam {} $".format(totalCost))
    printBars()
    print("{}".format(datetime.today().strftime('%Y/%m/%d %H:%M')))
    print("Online Market’imizi kullandıgınız için tesekkür ederiz!")

    # Stok miktarının uygun biçimde düşürülmesi
    for shoppingItemKey in shoppingCart.keys():
        inventory[shoppingItemKey][0] -= shoppingCart[shoppingItemKey][0]
    shoppingCart.clear()


def printMenu():
    print("1. Ürün ara\n2. Sepete git\n3. Satın al\n4. Oturum Kapat\n5. Çıkıs yap")
    serviceNumber = input("Seçiminiz: ")
    while(serviceNumber != 5):
        match serviceNumber:
            case "1":
                searchProduct()
            case "2":
                goToCart()
            case "3":
                purchase()
            case "4":
                login()
            case "5":
                return
            case _:
                print("Lütfen geçerli bir seçim yapınız.")
        print("1. Ürün ara\n2. Sepete git\n3. Satın al\n4. Oturum Kapat\n5. Çıkıs yap")
        serviceNumber = input("Seçiminiz: ")


def printCartMenu():
    print("Bir seçenegi seçiniz: ")
    print("1. Tutarı güncelleyin\n2. Bir ögeyi kaldırın\n3. Satın al\n4. ana menüye dön")


# main
login()
printMenu()
