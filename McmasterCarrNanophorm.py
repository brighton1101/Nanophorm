"""
McMasterCarr Invoice PDF Reader
Need PyPDF2 installed to work

Brighton Balfrey
Property of Nanophorm LLC

Shell code for project. Data is stored in list/variables
and users can then choose what they want to do with the 
information from there.

Name, price, line stored in InvoiceLine objects for
each item on invoice in list called INVOICE_ITEMS

Purchase Order # stored in purchaseOrder
Invoice # stored in invoicenum
Invoice date stored in invoicedate
Total stored in total
Merchandise total stored in merchandiseTotal
Shipping total stored in shippingTotal
Grand total stored in grandTotal

"""

import PyPDF2
#import csv if you want to alter to export into csv formats
#import csv

INVOICE_ITEMS = []
nextStr = ""

def handleFile(filename) :
    fileobj = open(filename, "rb")
    pdfReader = PyPDF2.PdfFileReader(fileobj)
    page = pdfReader.getPage(0)
    #PdfFileReader(open(filename, 'rb'))
    return page.extractText()



def program(filename) :

    purchaseOrder = ""
    total = ""
    invoicenum = ""
    invoicedate = ""

    subtotal = ""
    shipping = ""

    merchandiseTotal = ""
    shippingTotal = ""
    grandTotal = ""

    itemList = []

    page = handleFile(filename)
    notComplete = True
    stage = 0
    #while notComplete == True :
    #stage 0 extracts purchase number
    if stage == 0 :
        nextStr = page.split('Purchase Order ', 1)[1]
        strNum = extractNextNumber(nextStr)
        purchaseOrder = strNum
        page = page.split("Purchase Order ", 1)[1]
        stage = 1
    #stage 1 extracts total cost
    if stage == 1 :
        nextStr = page.split("Total $", 1)[1]
        strNum = extractNextNumber(nextStr)
        total = strNum
        page = page.split("Total $", 1)[1]
        stage = 2
    #stage 2 extracts invoice number
    if stage == 2 :
        nextStr = page.split("Invoice ", 1)[1]
        strNum = extractNextNumber(nextStr)
        invoicenum = strNum
        page = page.split("Invoice ", 1)[1]
        stage = 3
    #stage 3 extracts invoice date
    if stage == 3 :
        nextStr = page.split("Invoice Date ", 1)[1]
        strDate = extractDate(nextStr)
        invoicedate = strDate
        stage = 4
    #stage 4 extracts list of items
    if stage == 4 :
        nextStr = page.split("Total", 1)[1]
        q = []
        nextStr = extractItems(nextStr, "1", INVOICE_ITEMS)
        stage = 5
    if stage == 5 :
        nextStr = page.split("Merchandise ", 1)[1]
        merchandiseTotal = extractNextNumber(nextStr)
        nextStr = page.split("Shipping ", 1)[1]
        shippingTotal = extractNextNumber(nextStr)
        nextStr = page.split("Total $", 1)[1]
        grandTotal = extractNextNumber(nextStr)


        print("Purchase Order # " + purchaseOrder)
        print("Total " + total)
        print("Invoice # " +invoicenum)
        print("Invoice date: " + invoicedate)
        print("Items Ordered:")
        for a in INVOICE_ITEMS :
            print("Item name: " + a.name)
            print("Quantity: " + a.quantity)
            print("Price per: " + a.price)
        print("Merchandise Total: " + merchandiseTotal)
        print("Shipping Total: " + shippingTotal)
        print("Grand Total: " + grandTotal)
    if stage != 5 :
        print("ERROR")


            #break



class InvoiceLine:
    name = ""
    price = ""
    quantity = ""
    def getTotalPrice(self):
        p = float(self.price)
        q = float(self.quantity)
        return p*q


def extractItems(part, curr, info) :
    if part[0] != str(curr) :
        #return, this shit is done
        return part
    #handle first line
    poe = pack_or_each(part)
    if poe == "EACH" :
        firstpart = part.split("Each", 1)[0]
        secondpart = part.split("Each", 1)[1]
        numItems = ""
        name = ""
        price = ""
        i = len(firstpart) - 1 #i will reference firstpart
        j = 0 #j will reference secondpart
        #this is if the first parts order contained single digit num items
        if firstpart[i] == secondpart[j] and firstpart[i-1] +firstpart[i] != secondpart[j] + secondpart[j+1] :
            numItems = firstpart[i]
            #setname based off of this info
            q = 1
            while q < len(firstpart) - 1 :
                name += firstpart[q]
                q += 1
        #double digit numitems
        elif firstpart[i] != secondpart[j] and firstpart[i-1]+firstpart[i] == secondpart[j]+secondpart[j+1] :
            numItems = firstpart[i-1] +firstpart[i]
            q = 2
            while q < len(firstpart) - 2:
                name += firstpart[q]
                q += 1
        #triple digit numitems
        elif firstpart[i-2]+firstpart[i-1]+firstpart[i] == secondpart[j]+secondpart[j+1]+secondpart[j+2] :
            numItems = firstpart[i-2]+firstpart[i-1]+firstpart[i]
            q = 3
            while q < len(firstpart) - 3:
                name += firstpart[q]
                q += 1
        #now we have the name from the string firstpart and we know the number ordered
        #we just need price, which we find from secondpart by splitting at "Each"
        firstpart = secondpart.split("Each", 1)[0]
        secondpart = secondpart.split("Each", 1)[1]

        price = firstpart.split(numItems,1)[1]
        c = 0
        nprice = ""
        while c < len(price) :
            if c != 0:
                nprice += price[c]
            c += 1
        price = nprice

        # now we have everything to create our first object

        fitem = InvoiceLine()
        fitem.name = name
        fitem.price = price
        fitem.quantity = numItems
        info.append(fitem)

        # now we have to handle case where there is more than one item on invoice
        firstpart = secondpart.split(".", 1)[0]
        secondpart = secondpart.split(".",1)[1]

        part = secondpart[2:]


        currNum = int(curr)
        currNum += 1
        curr = str(currNum)
        nextStr = part
        return(extractItems(part, curr, info))

    if poe=="PER" : #should be poe == "PER"
        #start
        firstpart = part.split("Per",1)[0]
        thirdpart = part.split("Per",1)[1]

        firstpart = firstpart[::-1]
        secondpart = firstpart.split("kcaP", 1)[0]
        firstpart = firstpart.split("kcaP", 1)[1]

        firstpart=firstpart[::-1]
        secondpart=secondpart[::-1]
        price = ""
        quantity = ""
        name = ""
        if (secondpart[0] == "s") :
            #case where it says "Packs" aka more than 1 pack
            secondpart=secondpart[1:]
            i = len(secondpart) - 1
            price = ""
            q = 2
            while (secondpart[i] != "0" or q > 0) :
                price += secondpart[i]
                q -=1
                i -= 1
            price = price[::-1]
            i = i -1
            quantity = ""
            j = 0
            while j <= i :
                quantity += secondpart[j]
                j += 1

            nameLength = len(firstpart) - len(quantity)

            name = firstpart[1:nameLength]
        else :
            i = len(secondpart) - 1
            price = ""
            q = 2
            while (secondpart[i] != "0" or q > 0):
                price += secondpart[i]
                q -= 1
                i -= 1
            price = price[::-1]
            i = i - 1
            quantity = ""
            j = 0
            while j <= i:
                quantity += secondpart[j]
                j += 1

            nameLength = len(firstpart) - len(quantity)

            name = firstpart[0:nameLength]
        q=int(quantity)
        p=float(price)
        total=p*q
        totalStr = str(total)
        bad = thirdpart.split("Pack"+totalStr, 1)[0]
        newPart=thirdpart.split("Pack"+totalStr, 1)[1]
        item = InvoiceLine()
        item.quantity = quantity
        item.price = price
        item.name = name
        info.append(item)
        currNum = int(curr)
        currNum += 1
        curr = str(currNum)
        nextStr=newPart
        return(extractItems(newPart, curr, info))

def extractNextNumber(part) :
    strNum = ""
    i = 0
    while ( (ord(part[i]) >= 48 and ord(part[i]) <= 57) or ord(part[i]) == 46 ) :
        strNum += part[i]
        i += 1
    return strNum

def extractDate(part) :
    strNum = ""
    i = 0
    while ( (ord(part[i]) >= 48 and ord(part[i]) <= 57) or (ord(part[i]) == 47 or ord(part[i]) == 41) ):
        strNum += part[i]
        i += 1
    return strNum



class ProductLine:
    name = ""
    numShipped = -1
    pricePer = -1.0
    #productId = ""
    def getTotal(self):
        return self.numShipped * self.pricePer

#index_default and split_log_line taken from github
#find first instance of two strings
#https://stackoverflow.com/questions/28569765/split-by-the-delimiter-that-comes-first-python

def index_default(line, char):
    """Returns the index of a character in a line, or the length of the string
    if the character does not appear.
    """
    try:
        retval = line.index(char)
    except ValueError:
        retval = len(line)
    return retval

def pack_or_each(line):
    """Splits a line at either a period or a colon, depending on which appears
    first in the line.
    """
    packDist = index_default(line, "Per Pack")
    eachDist = index_default(line, "Each")
    if (packDist == len(line) and eachDist == len(line) ) :
        return "NEITHER"
    elif packDist < eachDist:
        return "PER"
    else:
        return "EACH"


program("C:/Users/Brighton/Documents/Nanophorm/invoice_2.PDF") #insert file path of pdf here
