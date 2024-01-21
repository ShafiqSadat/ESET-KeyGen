import subprocess

import telebot

LOGO = """
███████╗███████╗███████╗████████╗   ██╗  ██╗███████╗██╗   ██╗ ██████╗ ███████╗███╗   ██╗  
██╔════╝██╔════╝██╔════╝╚══██╔══╝   ██║ ██╔╝██╔════╝╚██╗ ██╔╝██╔════╝ ██╔════╝████╗  ██║   
█████╗  ███████╗█████╗     ██║      █████╔╝ █████╗   ╚████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║  
██╔══╝  ╚════██║██╔══╝     ██║      ██╔═██╗ ██╔══╝    ╚██╔╝  ██║   ██║██╔══╝  ██║╚██╗██║   
███████╗███████║███████╗   ██║      ██║  ██╗███████╗   ██║   ╚██████╔╝███████╗██║ ╚████║   
╚══════╝╚══════╝╚══════╝   ╚═╝      ╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝                                                                      
                                                https://t.me/LicenseForAll
"""

import modules.webdriver_installer as webdriver_installer
import modules.logger as logger

import modules.shared_tools as shared_tools
import modules.eset_register as eset_register
import modules.eset_keygen as eset_keygen
import modules.sec_email_api as sec_email_api

import traceback
import datetime
import sys
import os
import argparse
from subprocess import check_output, PIPE

def webdriver_installer_menu(edge=False): # auto updating or installing google chrome or microsoft edge webdrivers
    if edge:
        browser_name = 'Microsoft Edge'
    else:
        browser_name = 'Google Chrome'
    logger.console_log('-- WebDriver Auto-Installer --\n'.format(browser_name))
    if edge:
        browser_version = webdriver_installer.get_edge_version()
    else:
        browser_version = webdriver_installer.get_chrome_version()
    if browser_version is None:
        raise RuntimeError('{0} is not detected on your device!'.format(browser_name))
    current_webdriver_version = None
    platform = webdriver_installer.get_platform()[0]
    if edge:
        webdriver_name = 'msedgedriver'
    else:
        webdriver_name = 'chromedriver'
    if platform == 'win':
        webdriver_name += '.exe'
    if os.path.exists(webdriver_name):
        os.chmod(webdriver_name, 0o777)
        out = subprocess.check_output([os.path.join(os.getcwd(), webdriver_name), "--version"], stderr=subprocess.PIPE)
        if out is not None:
            if edge:
                current_webdriver_version = out.decode("utf-8").split(' ')[3]
            else:
                current_webdriver_version = out.decode("utf-8").split(' ')[1]
    logger.console_log('{0} version: {1}'.format(browser_name, browser_version[0]), logger.INFO, False)
    logger.console_log('{0} webdriver version: {1}'.format(browser_name, current_webdriver_version), logger.INFO, False)
    webdriver_path = None
    if current_webdriver_version is None:
        logger.console_log('\n{0} webdriver not detected, download attempt...'.format(browser_name), logger.ERROR)
    elif current_webdriver_version.split('.')[0] != browser_version[1]: # major version match
        logger.console_log('\n{0} webdriver version doesn\'t match version of the installed {1}, trying to update...'.format(browser_name, browser_name), logger.ERROR)
    if current_webdriver_version is None or current_webdriver_version.split('.')[0] != browser_version[1]:
        if edge:
            driver_url = webdriver_installer.get_edgedriver_download_url()
        else:
            driver_url = webdriver_installer.get_chromedriver_download_url()
        if driver_url is None:
            logger.console_log('\nCouldn\'t find the right version for your system!', logger.ERROR)
            if '--force' not in sys.argv:
                method = input('\nRun the program anyway? (y/n): ')
                if method == 'n':
                    return False
        else:
            logger.console_log('\nFound a suitable version for your system!', logger.OK)
            logger.console_log('\nDownloading...', logger.INFO)
            if webdriver_installer.download_webdriver('.', driver_url, edge):
                logger.console_log('{0} webdriver was successfully downloaded and unzipped!'.format(browser_name), logger.OK)
                webdriver_path = os.path.join(os.getcwd(), webdriver_name)
                if '--force' not in sys.argv:
                    input('\nPress Enter to continue...')
            else:
                logger.console_log('Error downloading or unpacking!', logger.ERROR)
                if '--force' not in sys.argv:
                    method = input('\nRun the program anyway? (y/n): ')
                    if method == 'n':
                        return False
    else:
        webdriver_path = os.path.join(os.getcwd(), webdriver_name)
    return webdriver_path

if __name__ == '__main__':
    logger.console_log(LOGO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', type=str, help='Token value')
    parser.add_argument('--channelID', type=str, help='ID value')
    parser.add_argument('--cli', type=bool, help='cli value')
    parser.add_argument('--bot', type=bool, help='bot value')
    parser.add_argument('--account', type=bool, help='account value')
    # Parse the command-line arguments
    args = parser.parse_args()

    # Retrieve the values
    token_value = args.token
    id_value = args.channelID
    is_bot = args.bot
    cli = args.cli
    cli_value = not cli
    try:
        driver = None
        if cli is True:
            cli_value = True
        account = args.account
        if cli is True:
            sys.argv.append('--force')
        if is_bot is True:
            bot = telebot.TeleBot(token_value, parse_mode='MARKDOWNv2')
        if '--firefox' in sys.argv:
            driver = shared_tools.initSeleniumWebDriver('firefox')
        else:
            chromedriver_path = chrome_driver_installer_menu()
            if chromedriver_path is not None:
                os.chmod(chromedriver_path, 0o777)
            driver = shared_tools.initSeleniumWebDriver('chrome', chromedriver_path)
        only_account = False
        if account is True:
            logger.console_log('\n-- Account Generator --\n')
            only_account = True
        else:
            logger.console_log('\n-- KeyGen --\n')
        email_obj = sec_email_api.SecEmail()
        logger.console_log('Mail registration...', logger.INFO)
        email_obj.register()
        logger.console_log('Mail registration completed successfully!', logger.OK)
        eset_password = shared_tools.createPassword(6)
        EsetReg = eset_register.EsetRegister(email_obj, eset_password, driver)
        EsetReg.createAccount()
        EsetReg.confirmAccount()
        driver = EsetReg.returnDriver()
        output_line = f'\nEmail: {email_obj.get_full_login()}\nPassword: {eset_password}\n'
        output_filename = 'ESET ACCOUNTS.txt'
        if not only_account:
            EsetKeyG = eset_keygen.EsetKeygen(email_obj, driver)
            EsetKeyG.sendRequestForKey()
            license_name, license_out_date, license_key = EsetKeyG.getLicenseData()
            output_line = f'\n🔸 Product: ||{license_name}||\n🕐 Expire: ||{license_out_date}||\n🔐 License: `{license_key}`\n'
            output_line1 = f'\n Product: {license_name}\n Expire: {license_out_date}\n License: {license_key}\n'
            output_filename = 'ESET KEYS.txt'
            if is_bot is True:
                bot.send_message(-1001219056300, output_line + "@LicenseForAll")
        logger.console_log(output_line)
        date = datetime.datetime.now()
        f = open(f"{str(date.day)}.{str(date.month)}.{str(date.year)} - "+output_filename, 'a')
        f.write(output_line1)
        f.close()
        driver.quit()
    except Exception as E:
        traceback_string = traceback.format_exc()
        if str(type(E)).find('selenium') and traceback_string.find('Stacktrace:') != -1: # disabling stacktrace output
            traceback_string = traceback_string.split('Stacktrace:', 1)[0]
        logger.console_log(traceback_string, logger.ERROR)
    if cli_value is False:
        input('Press Enter...')
