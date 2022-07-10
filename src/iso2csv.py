import xml.etree.ElementTree as ET
import xml
import sys
import pathlib

Finanzinstitut = sys.argv[1]
FileInput = sys.argv[2]
Pfad = pathlib.Path(FileInput).parent.absolute()
Datei = pathlib.Path(FileInput).absolute()
Dateiname = pathlib.Path(FileInput).stem
FileOutput = str(Pfad)+'/../csv/'+str(Dateiname)+'.csv'
# print(FileOutput)
FileOutputStream = open(FileOutput, 'w')

# Python XML Parsing
root = ET.parse(FileInput).getroot()
tag = root.tag
# print(tag)

namespace = str(root.tag).replace("Document", "")
# print(namespace)

# iterate over all the nodes with tag name - holiday
for rootElement in root:

    for Statement in rootElement.findall(namespace+'Stmt'):

        # Auslesen des Kontos und des Inhabers
        for Acct in Statement.findall(namespace+"Acct"):
            #print("\n********************* Konto *********************")
            for Account in Acct.findall(namespace+"Id"):
                Konto = Account.find(namespace+"IBAN").text
            #    print(Konto)
            for Owner in Acct.findall(namespace+"Ownr"):
                Inhaber = Owner.find(namespace+"Nm").text
            #    print(Inhaber)
#            for Svcr in Acct.findall(namespace+"Svcr"):
#                for FinInstnId in Svcr.findall(namespace+"FinInstnId"):
#                    Finanzinstitut = FinInstnId.find(namespace+"Nm").text
#                print(Inhaber)

        # print(str(Statement.tag).replace(namespace,""))
        # print(Element)
        # print('Ebene 1')

        # Ab hier kommen die einzelnen Buchungen Ntry
        for Entry in Statement.findall(namespace+"Ntry"):
            # print(str(Entry.tag).replace(namespace,""))
            # print("\n********************* Buchung *********************")
            #            for bookingdate in Entry.find(namespace+"BookgDt"):
            # Buchungsdatum in BookgDt unter Dt auslesen
            for bookingdate in Entry.findall(namespace+"BookgDt"):
                BookDate = bookingdate.find(namespace+"Dt").text

            # Buchungstext auslesen
            AddtlNtryInf = Entry.find(namespace+'AddtlNtryInf').text

            # Mitteilung auslesen  ***** Hier sollte noch der Zusatz unter TxDtls > RmtInf > Ustrd eingetragn werden
            # UserTxDetails muss leer sein weil nicht immer etwas in diesem Feld steht, bzw. es ist gar nicht vorhanden
            UserTxDetails = ""
            for EntryDetails in Entry.findall(namespace+"NtryDtls"):
                for TxDetails in EntryDetails.findall(namespace+"TxDtls"):
                    for RemoteInfo in TxDetails.findall(namespace+"RmtInf"):
                        if (RemoteInfo.find(namespace+"Ustrd")) is not None:
                            UserTxDetails = RemoteInfo.find(namespace+"Ustrd").text

            #print(Konto+';'+BookDate+';'+AddtlNtryInf.replace("\n", " ") + ' ' + UserTxDetails.replace("\n", " "), end = '')
            FileOutputStream.write(Konto+';'+BookDate+';'+AddtlNtryInf.replace(
                "\n", " ") + ' ' + UserTxDetails.replace("\n", " "))

            # Amt: Betrag mit Währung Ccy
            Amt = Entry.find(namespace+'Amt').text
            Currency = Entry.find(namespace+"Amt").attrib.get('Ccy')
            # CdtDbtInd: Credit or Debit
            CdtDbtInd = Entry.find(namespace+"CdtDbtInd").text

            # Wenn Debit, dann Minus
            if CdtDbtInd == 'DBIT':
                #print(";"+Finanzinstitut +';'+Inhaber+';-' + Amt+';'+ Currency, end = '')
                FileOutputStream.write(
                    ';'+Finanzinstitut + ';'+Inhaber + ';'+' -' + Amt + ';' + Currency)
                #print('  '+'unknown'+'  ' + Amt, Currency)
                #FileOutputStream.write('  '+'unknown'+'  ' + Amt + ' ' + Currency + '\n')
            # Wenn Credit, dann Plus
            else:
                #print(';'+Finanzinstitut + ';'+Inhaber+';'+Amt+';'+ Currency, end = '')
                FileOutputStream.write(
                    ';'+Finanzinstitut + ';'+Inhaber + ';'+Amt + ';' + Currency)
                #print(' '+'unknown'+'  -' + Amt, Currency, end = '')
                #FileOutputStream.write('  '+'unknown'+'  -' + Amt + ' ' + Currency)
            # print('\n')
            FileOutputStream.write('\n')

"""
            print("\n\n********************* unordentlich *********************")

            for element in Entry:
                attributes = element.attrib
                print(attributes)
                Amt = element.find(namespace+'Amt')
                print('Betrag: ', Amt)

                el_name = str(element.tag).replace(namespace,"")
                el_value = str(Entry.find(element.tag).text).replace(namespace,"")
                print(el_name, ' : ', el_value)
                if el_name == "AddtlNtryInf":
                    print(el_name, " : ", str(el_value).replace("\n"," "))

"""
# print(Statement)

FileOutputStream.close()
