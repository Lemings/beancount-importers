import dateutil
from beancount.core import data

import beangulp
from beancount_importers.bank_classifier import payee_to_account_mapping
from beangulp.importers import csv
from csv import register_dialect, Dialect
from typing import Callable, Dict, List, Optional, Union
from beangulp import cache
from beangulp import utils
from beancount import Amount

Col = csv.Col

# PYTHONPATH=.:beangulp python3 import_wise.py <csv_file> > wise.bean

ATEGORY_TO_ACCOUNT_MAPPING = {
    "Eating out": "Expenses:EatingOut",
    "Groceries": "Expenses:Groceries",
    "Shopping": "Expenses:Shopping",
    "Accommodation": "Expenses:Accommodation",
    "Bills": "Expenses:Bills",
    "Hobbies": "Expenses:Hobbies",
    "Wellness": "Expenses:Wellness",
    "Transport": "Expenses:Transport",
    "Travel": "Expenses:Travel",
    "Entertainment": "Expenses:Entertainment",
    "Donations": "Expenses:Donations",
}
TRANSACTIONS_CLASSIFIED_BY_ID = {
    "CARD-XXXXXXXXX": "Expenses:Shopping",
}

# UNCATEGORIZED_EXPENSES_ACCOUNT = "Expenses:Uncategorized:Wise"
UNCATEGORIZED_EXPENSES_ACCOUNT = "Expenses:FIXME"


def categorizer(txn, row):
    transaction_id = row[0]
    payee = row[4]
    comment = row[9]
 #   note = row[17]
    drcr = row[14]

    posting_account = None
    # Expenses
    if drcr == "D":

        if "zoobums" in payee.lower():
            posting_account = "Expenses:Suns:Barība:Zoobums"

        if "decathlon riga" in payee.lower():
            posting_account = "Expenses:Apģērbs:Decathlon"

        if "pepco" in payee.lower():
            posting_account = "Expenses:Apģērbs:PEPCO"

        if "sinsay" in payee.lower():
            posting_account = "Expenses:Apģērbs:Sinsay"

        if "x jeans" in payee.lower():
            posting_account = "Expenses:Apģērbs:X-jeans"

        if "h&m" in payee.lower():
            posting_account = "Expenses:Apģērbs:H-un-M"

        if "maxima" in payee.lower() and "aizkraukle" in comment.lower():
            posting_account = "Expenses:Pārtika:Maxima:Aizkraukle"

        if "rimi" in payee.lower() and "salaspils" in comment.lower():
            posting_account = "Expenses:Pārtika:Rimi:Salaspils"
        if "rimi" in payee.lower() and "aizkraukle" in comment.lower():
            posting_account = "Expenses:Pārtika:Rimi:Aizkraukle"
        if "rimi" in payee.lower() and "Saga" in comment.lower():
            posting_account = "Expenses:Pārtika:Rimi:Sāga"
        if "rimi" in payee.lower() and "alfa" in comment.lower():
            posting_account = "Expenses:Pārtika:Rimi:Alfa"

        if "lidl" in payee.lower() and "eizens" in comment.lower():
            posting_account = "Expenses:Pārtika:LIDL:Eizenšteina"
        if "lidl" in payee.lower() and "ogre" in comment.lower():
            posting_account = "Expenses:Pārtika:LIDL:Ogre"
        if "lidl" in payee.lower() and "salaspils" in comment.lower():
            posting_account = "Expenses:Pārtika:LIDL:Salaspils"

        if "top aizkraukle" in payee.lower():
            posting_account = "EXpenses:Pārtika:TOP:Aizkraukle"

        if "t" in payee.lower() and "kursi" in comment.lower() and "aizkraukle" in comment.lower():
            posting_account = "Expenses:Remonts:Kursi:Aizkraukle"
        if "melanija" in payee.lower():
            posting_account = "Expenses:Pārtika:Saldumi"
        if "ik efaly" in payee.lower():
            posting_account = "Expenses:Pārtika:Tirgus"
        if "IKEA LATVIA RESTORANS" in payee:
            posting_account = "Expenses:Pārtika:Ikea"

        if "DEPO-VEIKALS-KRASTA" in payee:
            posting_account = "Expenses:Remonts:Depo:Krasta"
        if "depo-veikals-bergi" in payee.lower():
            posting_account = "Expenses:Remonts:Depo:Berģi"
        if "depo" in payee.lower() and "marupe" in comment.lower():
            posting_account = "Expenses:Remonts:Depo:Mārupe"
        if "depo" in payee.lower() and "dreilini" in comment.lower():
            posting_account = "Expenses:Remonts:Depo:Dreiliņi"

        if "ksenukai lucavsala" in payee.lower():
            posting_account = "Expenses:Remonts:Ksenukai:Lucavsala"
        if "ksenukai ozols" in payee.lower():
            posting_account = "Expenses:Remonts:Ksenukai:Ozols"

        if "drogas" in payee.lower() and "aizkraukle" in comment.lower():
            posting_account = "Expenses:Kosmētika:Drogas:Aizkraukle"
        if "hottt" in payee.lower() and "aizkraukle" in comment.lower():
            posting_account = "Expenses:Saimniecības-preces:Hott:Aizkraukle"

        if "majai un darzam" in payee.lower() and "aizkraukle" in comment.lower():
            posting_account = "Expenses:Saimniecības-preces:Mājai-un-dārzam:Aizkraukle"

        if "virsi" in payee.lower() and "aizkraukle" in comment.lower():
            posting_account = "Expenses:Auto:Degviela:Virsi:Aizkraukle"

        if "sia skrīveru saimnieks" in payee:
            posting_account = "Expenses:Māja:Ūdens"
        if "latvenergo" in payee:
            posting_account = "Expenses:Māja:Elektrība"

        if "ĶILUPE SIA" in payee:
            posting_account = "Expenses:Māja:Atkritumi"

        if "IKEA LATVIA-VEIKALS" in payee:
            posting_account = "Expenses:Mēbeles:Ikea"

        if "seb banka" in payee.lower() and "mēneša maksa" in comment.lower():
            posting_account = "Expenses:SEB:Mēneša-maksa"
        if "seb banka" in payee.lower() and "komisija" in comment.lower():
            posting_account = "Expenses:SEB:Komisija"
        if "seb banka" in payee.lower() and "vp.m.kom" in comment.lower():
            posting_account = "Expenses:SEB:Komisija"
        if "seb banka" in payee.lower() and "apkalpošanas" in comment.lower():
            posting_account = "Expenses:SEB:Apkalpošanas-maksa"
        if "seb banka" in payee.lower() and "iedzīvotāju ienākuma nodoklis no procentiem" in comment.lower():
            posting_account = "Expenses:Nodokļi:Ienākuma-nodoklis-no-procentiem"
        if "SEB Life and Pension Baltic SE" in payee:
            posting_account = "Expenses:Apdrošināšana:Apgādnieka-zaudēšana"

        if "tet" in payee.lower():
            posting_account = "Expenses:Televīzija:TET"

        if "fonds ziedot.lv" in payee.lower():
            posting_account = "Expenses:Ziedojums"
        if "biedrība radio marija latvija" in payee.lower():
            posting_account = "Expenses:Ziedojums"

        if "atm" in payee.lower() and "izmaksa" in comment.lower():
            posting_account = "Assets:Skaidra nauda"

        # Specific transactions
        if transaction_id in TRANSACTIONS_CLASSIFIED_BY_ID:
            posting_account = TRANSACTIONS_CLASSIFIED_BY_ID[transaction_id]

        # Default by category
        if not posting_account:
            posting_account = UNCATEGORIZED_EXPENSES_ACCOUNT

        account = txn.postings[0].account
        amount = txn.postings[0].units.number

        newAmount = Amount(-1 * amount, "EUR")

        txn.postings[0] = data.Posting(
            account, newAmount, None, None, None, None)

        txn.postings.append(
            data.Posting(posting_account, Amount(
                amount, "EUR"), None, None, None, None)
        )
    if drcr == "C":
        if "seb banka" in payee.lower() and "izmaksātie procenti" in comment.lower():
            posting_account = "Income:Izmaksatie-procenti"
        if "as latvenergo" in payee.lower() and "darba alga" in comment.lower():
            posting_account = "Income:Alga"
        if "sociālais dienests" in payee.lower() and "ikmēneša pabalsts" in comment.lower():
            posting_account = "Income:Pabalsts"
        # test = payee_to_account_mapping

        # print(type(test))
        # Custom
        # if payee == "Some Gym That Sells Food":
        #     if txn.postings[0].units.number < -40:
        #         posting_account = "Expenses:Wellness"
        #     else:
        #         posting_account = "Expenses:EatingOut"

        # Classify transfers
        # if payee.lower() == "your name":
        #     if "Revolut" in comment:
        #         posting_account = "Assets:Revolut:Cash"
        #     else:
        #         posting_account = "Assets:Wise:Cash"
        # elif payee == "Broker":
        #     posting_account = "Assets:Broker:Cash"
        # elif payee.lower() == "some dude":
        #     posting_account = "Liabilities:Shared:SomeDude"

        # if comment.endswith("to my savings jar"):
        #     posting_account = "Assets:Wise:Savings:USD"

        # Default by category
        if not posting_account:
            posting_account = UNCATEGORIZED_EXPENSES_ACCOUNT

        txn.postings.append(
            data.Posting(posting_account, -
                         txn.postings[0].units, None, None, None, None)
        )
        #    if note:
        #        txn.meta["comment"] = note
        #    print(txn)
    return txn


def get_importer(account, currency):
    # "MU NR.";
    # "DATUMS";
    # "MAKSĀJUMA VALŪTA";
    # "MAKSĀJUMA SUMMA";
    # "PARTNERA NOSAUKUMS";
    # "PARTNERA PERS. KODS/ REĢ. NR.";
    # "PARTNERA KONTS";
    # "PARTNERA BANKA";
    # "PARTNERA BANKAS SWIFT KODS";
    # "MAKSĀJUMA MĒRĶIS";
    # "TRANSAKCIJAS NUMURS";
    # "DOKUMENTA DATUMS";
    # "TRANSAKCIJAS TIPS";
    # "REFERENCE";
    # "DEBETS/ KREDĪTS";
    # "SUMMA KONTA VALŪTĀ";
    # "KONTA NR.";
    # "KONTA VALŪTA";
    register_dialect('seb', 'excel', delimiter=';')
    return csv.CSVImporter(
        {
            Col.DATE: "DATUMS",
            Col.NARRATION: "MAKSĀJUMA MĒRĶIS",
            Col.AMOUNT: "MAKSĀJUMA SUMMA",
            Col.PAYEE: "PARTNERA NOSAUKUMS",
            Col.CATEGORY: "PARTNERA NOSAUKUMS",
            Col.REFERENCE_ID: "TRANSAKCIJAS NUMURS",
            Col.DRCR: "DEBETS/ KREDĪTS"

        },
        account,
        currency,
        skip_lines=1,
        categorizer=categorizer,
        debug=False,
        csv_dialect="seb",

        dateutil_kwds={
            "parserinfo": dateutil.parser.parserinfo(dayfirst=True)},
    )


if __name__ == "__main__":
    ingest = beangulp.Ingest(
        [get_importer("Assets:SEB:Debetkarte", "EUR")], [])
    ingest()
