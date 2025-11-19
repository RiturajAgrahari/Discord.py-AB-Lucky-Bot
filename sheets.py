import os
import platform
import discord

from dotenv import load_dotenv
# Service Account
from googleapiclient.discovery import build
from google.oauth2 import service_account
from models import Profile, BotUsage, Review, TodayLuck


SERVICE_ACCOUNT_FILE = 'service.json'
ALPHABETS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Loading Environment Variables.
load_dotenv()


# If it is in production run it on debug to avoid unnecessary functionality and tests
DEBUG = False if platform.system() == 'Linux' else True


if DEBUG:
    # TEST GOOGLE SHEETS :
    SPREADSHEET_ID = "1LZOAtgaakwNt016Mg0RY45QgK4KCl8BMpKY1hduSjXk"
else:
    # CLIENT'S GOOGLE SHEETS :
    SPREADSHEET_ID = os.getenv('SPREADSHEET_ID', None)


class GoogleSheets:
    """Google Sheets Class to handle all operation"""

    def __init__(self):
        """Initializing Google sheets API operational object"""

        # Logging
        print(f'[ Execution ] Instantiating Google Sheets.')

        # Initializing the attribute
        self.creds = None  # sheets credentials
        self.range: str = "A2:Z20"  # Spreadsheet range
        self.sheet = None  # spreadsheet instance
        self.values = []  # Cell data
        self.headers: list[str] = []  # Header Cell data
        self.header_range: str = "A1:Z1"  # Spreadsheet header range

        # Authenticating to the Google sheets.
        self.creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )

        # Logging.
        print(f'[ Completed ] Authentication Completed with Google Sheets.')

    async def connect_to_sheet(self):
        """Establishing connection to the spreadsheet."""
        try:
            # Logging.
            print(f'[ Execution ] Connecting to Google Sheets...')

            # Building the sheets.
            service = build("sheets", "v4", credentials=self.creds)

            # Call the Sheets API.
            self.sheet = service.spreadsheets()

            # Logging.
            print(f'[ Completed ] Connection Established with Google Sheets.')

        # Handling Exception.
        except Exception as e:
            print(e)

    async def set_range(self, header, sheet):
        print('[ Execution ] Creating header for model Profile...')
        # Updating header range:
        self.header_range: str = f"A1:D1"
        self.header_range: str = f"A1:{ALPHABETS[len(header) - 1]}1"
        self.range.replace('Z', ALPHABETS[len(header) - 1])
        # Creating a header in sheets
        self.sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{sheet}!{self.header_range}",
            valueInputOption="USER_ENTERED",
            body={"values": [header]}).execute()
        # Logging.
        print(f'[ Completed ] Spreadsheet header created.')

    async def inserting_data(self, data, sheet):
        # Logging.
        print(f'Insert data in {sheet}...')
        # Creating a new row in sheets
        self.sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{sheet}!A2:{self.range[3]}{len(data) + 1}",
            valueInputOption="USER_ENTERED",
            body={"values": data}
        ).execute()
        # Logging
        print(f'Insertion completed.')

    async def sync_profile_data(self):
        """Set spreadsheet header if not exists otherwise report the existing scenario"""

        sheet = 'profile'

        await self.set_range(
            header=["id", "discord_name", "discord_id", "bot_used"],
            sheet=sheet
        )

        # Fetching feedback information.
        profiles = await Profile.all().order_by('id')

        # IF feedback information is available in database.
        if profiles:

            # Trying to add a row in spreadsheet.
            try:
                profile_data = [
                    [
                        str(profile.id),
                        str(profile.discord_name),
                        str(profile.discord_id),
                        str(profile.bot_used)
                    ] for profile in profiles
                ]

                await self.inserting_data(data=profile_data, sheet=sheet)

            except Exception as e:
                print(e)

        else:
            # Logging.
            print(f"No {sheet} information in database")

    async def sync_botusage_data(self):
        """Set spreadsheet header if not exists otherwise report the existing scenario"""

        sheet = 'botusage'

        await self.set_range(
            header=["id", "date", "fandom_bot", "lucky_bot", "rpg_bot"],
            sheet=sheet
        )

        # Fetching feedback information.
        bot_usages = await BotUsage.all().order_by('date')

        # IF feedback information is available in database.
        if bot_usages:

            # Trying to add a row in spreadsheet.
            try:
                usage_data = [
                    [
                        str(usage.id),
                        str(usage.date),
                        str(usage.fandom_bot),
                        str(usage.lucky_bot),
                        str(usage.rpg_bot)
                    ] for usage in bot_usages
                ]

                await self.inserting_data(data=usage_data, sheet=sheet)

            except Exception as e:
                print(e)

        else:
            # Logging.
            print(f"No {sheet} information in database")

    async def sync_review_data(self):
        """Set spreadsheet header if not exists otherwise report the existing scenario"""

        sheet = 'review'

        await self.set_range(
            header=["id", "profile id", "review", "star_rating", "reviewed_on"],
            sheet=sheet
        )

        # Fetching feedback information.
        reviews = await Review.all().prefetch_related('uid').order_by('reviewed_on')

        # IF feedback information is available in database.
        if reviews:

            # Trying to add a row in spreadsheet.
            try:
                review_data = [
                    [
                        str(review.id),
                        str(review.uid.id),
                        str(review.review),
                        str(review.star_rating),
                        str(review.reviewed_on)
                    ] for review in reviews
                ]

                await self.inserting_data(data=review_data, sheet=sheet)

            except Exception as e:
                print(e)

        else:
            # Logging.
            print(f"No {sheet} information in database")

    async def sync_todayluck_data(self):
        """Set spreadsheet header if not exists otherwise report the existing scenario"""

        sheet = 'todayluck'

        await self.set_range(
            header=["id", "profile id", "location", "container", "weapon", "item", "summary"],
            sheet=sheet
        )

        # Fetching feedback information.
        lucks = await TodayLuck.all().prefetch_related('uid').order_by('id')

        # IF feedback information is available in database.
        if lucks:

            # Trying to add a row in spreadsheet.
            try:
                luck_data = [
                    [
                        str(luck.id),
                        str(luck.uid.id),
                        str(luck.location),
                        str(luck.container),
                        str(luck.weapon),
                        str(luck.item),
                        str(luck.summary)
                    ] for luck in lucks
                ]

                await self.inserting_data(data=luck_data, sheet=sheet)

            except Exception as e:
                print(e)

        else:
            # Logging.
            print(f"No {sheet} information in database")
