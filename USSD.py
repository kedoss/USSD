import json
from pathlib import Path
from datetime import datetime

PRODUCTS_FILE = Path("ibidandazwa.json")
SALES_FILE = Path("ivyadandajwe.json")

def load_products():
    if PRODUCTS_FILE.exists():
        with PRODUCTS_FILE.open('r') as f:
            return json.load(f)
    return []

def save_products(products):
    with PRODUCTS_FILE.open('w') as f:
        json.dump(products, f, indent=4)

def load_data(filename):
    path = Path(filename)
    if path.exists():
        with path.open('r') as f:
            return json.load(f)
    return []

def save_data(filename, data):
    path = Path(filename)
    with path.open('w') as f:
        json.dump(data, f, indent=4)

ibidandazwa = load_products()
ivyadandajwe = load_data(SALES_FILE)

Menu = """1. kuraba ibidandazwa
2. gushiramwo ikidandazwa
3. guhanagura ikidandazwa
4. guhindura ibiranga ikidandazwa
5. kudandaza
6. kuraba ivyadandajwe
7. kuraba raporo
0. Guhagarika"""

kora = {
    "1": "kuraba ibidandazwa",
    "2": "gushiramwo ikidandazwa",
    "3": "guhanagura ikidandazwa",
    "4": "guhindura ibiranga ikidandazwa",
    "5": "kudandaza",
    "6": "kuraba ivyadandajwe",
    "7": "kuraba raporo",
    "0": "Guhagarika"
}

def gushiramwo():
    print("\nGushiramwo ikidandazwa gishasha")
    
    izina = input("Injiza izina ry'ikidandazwa: ")
    
    for product in ibidandazwa:
        if product['izina'].lower() == izina.lower():
            print("Iki kidandazwa gisanzwe gihari!!!")
            return
    
    try:
        igiciro = int(input("Injiza igiciro: "))
        igitigiri = int(input("Injiza igitigiri: "))
        
        new_id = max(p['id'] for p in ibidandazwa) + 1 if ibidandazwa else 1
        
        new_product = {
            "id": new_id,
            "izina": izina,
            "igiciro": igiciro,
            "igitigiri": igitigiri
        }
        
        ibidandazwa.append(new_product)
        save_products(ibidandazwa)
        print(f"{izina} wagiye mubidandazwa!")
        
    except ValueError:
        print("oloha")


def kuraba():
    print("\nIbidandazwa:")
    if not ibidandazwa:
        print("Nta bidandazwa bihari.")
    else:
        print("ID | Izina       | Igiciro | Igitigiri")
        for product in ibidandazwa:
            print(f"{product['id']:2} | {product['izina']:10} | {product['igiciro']:7} | {product['igitigiri']:7}")

def kudandaza():
    print("\nKudandaza")
    kuraba()
    
    if not ibidandazwa:
        return
    
    try:
        product_id = int(input("Injiza ID y'ikidandazwa: "))
        quantity = int(input("Injiza igitigiri: "))
        
        product = None
        for p in ibidandazwa:
            if p['id'] == product_id:
                product = p
                break
                
        if not product:
            print("Iyi ID ntibaho!")
            return
            
        if quantity <= 0:
            print("Injiza igitigiri kiruta 0")
            return
            
        if quantity > product['igitigiri']:
            print(f"warenze kugitigiri gisigaye! Igitigiri gisigaye: {product['igitigiri']}")
            return
            
        sale = {
            "date": datetime.now().strftime("%d/%m %Hh%M"),
            "product_id": product_id,
            "izina": product['izina'],
            "igiciro": product['igiciro'],
            "quantity": quantity,
            "total": product['igiciro'] * quantity
        }
        
        product['igitigiri'] -= quantity
        ivyadandajwe.append(sale)
        
        save_data(PRODUCTS_FILE, ibidandazwa)
        save_data(SALES_FILE, ivyadandajwe)
        
        print(f"\n{quantity} {product['izina']} wadandajwe neza!")
        print(f"Total: {sale['total']} ")
        
    except ValueError:
        print("Injiza ivy'ukuri!")

def kuraba_ivyadandajwe():
    print("\nKuraba ivyadandajwe")
    
    if not ivyadandajwe:
        print("Nta kidandazwa kiradandazwa.")
        input("\nFyonda 0 gusubira ku ntango: ")
        return
    
    print("\nInjiza itariki (dd/mm) canke 0 gusubiramwo:")
    date_input = input("Itariki: ")
    
    if date_input == "0":
        return
    
    total = 0
    print("\nIvyadandajwe:")
    
    for sale in ivyadandajwe:
        if date_input in sale["date"]:
            print(f"{sale['date']} {sale['izina']:10} x {sale['quantity']} : {sale['total']:6,}".replace(",", " "))
            total += sale['total']
    
    if total > 0:
        print(f"{' ':20} vyose hamwe : {total:6,}".replace(",", " "))
    else:
        print("Nta kidandazwa cadandajwe kuri iyo tariki")
    
    input("\nFyonda 0 gusubira ku ntango: ")

def kuraba_raporo():
    print("\nRaporo:")
    
    total_ventes = len(ivyadandajwe)
    total_revenu = sum(sale['total'] for sale in ivyadandajwe)
    produits_epuises = sum(1 for p in ibidandazwa if p['igitigiri'] == 0)
    total_produits = len(ibidandazwa)
    
    print(f"Mumaze kudandaza incuro    {total_ventes:10}")
    print(f"Mumaze kudandaza amahera   {total_revenu:10,}".replace(",", " "))
    print(f"ibidandazwa vyaheze       {produits_epuises:10}")
    print(f"Ibidandazwa vyose hamwe    {total_produits:10}")
    
    input("\nFyonda 0 gusubira ku ntango: ")


print("Hitamwo: ")
while True:
    print(Menu)
    choix = input("Injiza igiharuro: ")
    
    if choix in kora:
        if choix == "0":
            print("Murakoze gukoresha USSD.")
            break
        elif choix == "1":
            kuraba()
        elif choix == "2":
            gushiramwo()
        elif choix == "5":
            kudandaza()
        elif choix == "6":
            kuraba_ivyadandajwe()
        elif choix == "7":
            kuraba_raporo()
    else:
        print("Injiza igiharuro kiri hagati ya 0 na 7")
    
    input("\nFyonda Entrer kugira usubire...")