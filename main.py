from PIL import Image
import csv

baseFilePath = "C:\\Users\\Roey Shapiro\\Documents\\AAB Backup\\College\\Year 3\\Set\\DeckOfDecks\\"
cardData: dict[int, int] = {}
outOfBoundsValue = 1000
pageDims = (2000, 2828)
cardDimsOnPage = (623, 869)

def createPages():
    x = 0
    y = 0
    currentPageIndex = 0
    cardsOnPage = 0
    totalCards = 0
    fullPage = Image.new(mode="RGB", size=pageDims, color=(255, 255, 255))
    for cardFilePath, numCopies in cardData.items():
        try:
            rawCard = Image.open(f"{baseFilePath}images\\{cardFilePath}.png")
            card = rawCard.resize(cardDimsOnPage)
            for c in range(numCopies):
                fullPage.paste(card, (x * cardDimsOnPage[0], y * cardDimsOnPage[1]))

                x += 1
                if x == 3:
                    x = 0
                    y += 1

                cardsOnPage += 1
                totalCards += 1
                if cardsOnPage == 9:
                    fullPage = SavePage(fullPage, currentPageIndex)
                    x = 0;
                    y = 0
                    cardsOnPage = 0
                    currentPageIndex += 1
        except:
            print(f"An image for card #{cardFilePath} couldn't be found.")




    if cardsOnPage < 9:
        SavePage(fullPage, currentPageIndex)

    return currentPageIndex + 1, totalCards

def GetSpreadSheetData():
    with open(baseFilePath + "Formatter\\MTGCard\\DOD.csv") as file:
        csvReader = csv.DictReader(file)
        for row in csvReader:
            rowIndex = ParseNullableInt(row["INDEX"])
            if 0 < rowIndex < outOfBoundsValue:
                cardData[rowIndex] = ParseNullableInt(row["#"])


def ParseNullableInt(string):
    if len(string) == 0:
        return outOfBoundsValue
    return int(string)

def SavePage(page, currentPageIndex):
    page.save(f"{baseFilePath}final pages\\page_{currentPageIndex}.png", quality=95)
    return Image.new(mode="RGB", size=pageDims, color=(255, 255, 255))

if __name__ == '__main__':
    print("Running...")
    print("Populating card data from spreadsheet...")
    GetSpreadSheetData()
    # cardData = {1: 7, 2: 4, 3: 3}
    print("Creating page images...")
    numPages, totalCards = createPages()
    print(f"... Done! Created {numPages} pages with {totalCards} out of a total of {sum(cardData.values())} total cards on them.")
