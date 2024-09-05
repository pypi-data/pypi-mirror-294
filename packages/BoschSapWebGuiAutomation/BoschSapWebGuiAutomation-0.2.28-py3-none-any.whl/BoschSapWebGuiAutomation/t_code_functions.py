from .common_functions import *


def get_fb03_functions(browser: Firefox, wait: WebDriverWait):
    """This function is used to get functions of t-code fb03

    Args:
        browser(Firefox): This is the webdriver instance
        wait(WebDriverWait): This is the WebDriverWait instance

    """
    return FB03Functions(browser, wait)


def get_ff5_functions(browser: Firefox, wait: WebDriverWait):
    """This function is used to get functions of t-code ff5

    Args:
        browser(Firefox): This is the webdriver instance
        wait(WebDriverWait): This is the WebDriverWait instance

    """
    return FF5Functions(browser, wait)


class FB03Functions(WebSapCommonFunctions):
    """This class is used to process special function of t-code fb03

    Args:
        WebSapCommonFunctions (class): This is the class that contains web sap general functions
    """

    def __init__(self, browser, wait):
        """This function is used to initial parameters

        Args:
            browser(Firefox): This is the webdriver instance
            wait(WebDriverWait): This is the WebDriverWait instance
        """
        super().__init__()
        self.browser = browser
        self.wait = wait

    def click_store_business_attachment(self, document_file_path_dict: dict, window_class: str, window_name: str, insert_function: bool = False,
                                        inserted_function=None, **kwargs):
        """This function is used to click store business attachment selection and upload related documents

        Args:
            insert_function(bool): This is the flag whether to insert function with click_store_business_attachment
            inserted_function(function): This is the function instance name
            window_class(str): This is the class of window
            window_name(str): This is the window title
            document_file_path_dict(dict): This is the dict of document file path and document file format

        """
        # click add attachment button
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, UPLOAD_ATTACHMENT_BUTTON_CSS_SELECTOR)))
        sleep(2)
        self.click_or_input_by_css_selector(UPLOAD_ATTACHMENT_BUTTON_CSS_SELECTOR, 'click')
        sleep(2)
        # click Create...
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, CREATE_CSS_SELECTOR)))
        create_element = self.browser.find_element(By.CSS_SELECTOR, CREATE_CSS_SELECTOR)
        ActionChains(self.browser).move_to_element(create_element).click().perform()
        sleep(2)
        # click Store business document selection
        self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, UPLOAD_ATTACHMENT_CHOICES_CSS_SELECTOR)))
        upload_elements = self.browser.find_elements(By.CSS_SELECTOR, UPLOAD_ATTACHMENT_CHOICES_CSS_SELECTOR)
        row_index = 1
        for upload_element in upload_elements:
            upload_text = upload_element.find_element(By.CSS_SELECTOR, UPLOAD_ATTACHMENT_TEXT_CSS_SELECTOR).text.strip()
            if upload_text == 'Store business document':
                self.click_or_input_by_css_selector(
                    f'div#menu_1_1_bp div.lsMnuCnt table.lsMnuTable tr:nth-child({row_index}) td.urMnuTxt span',
                    'click')
                break
            row_index += 1
        sleep(2)
        self.wait_invisibility_of_loading_window()
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, UPLOAD_ATTACHMENT_DOCUMENT_TYPES_OVERVIEW_CSS_SELECTOR)))
        # upload documents
        for document_file_path, document_file_format in document_file_path_dict.items():
            self.upload_document_number_attachments(document_file_path, document_file_format, window_class, window_name)
            print('---------- Upload Successfully ----------')
            print(f'{document_file_path}')
            if insert_function:
                inserted_function(document_file_path, **kwargs)

        # close upload window
        self.wait_invisibility_of_loading_window()
        self.click_or_input_by_css_selector(UPLOAD_ATTACHMENT_COMPLETE_CSS_SELECTOR, 'click')
        sleep(1)

    def upload_document_number_attachments(self, file_path: str, file_format: str, window_class: str, window_name: str,
                                           target_document_type_dict: dict = TARGET_DOCUMENT_DICT):
        """This function is used to upload attachment for each document number

        Args:
            file_format(str): This is the file format of file. e.g. JPG, PDF, MSG
            window_class(str): This is the class of window
            window_name(str): This is the window title
            file_path(str): This is the file path that need to be uploaded
            target_document_type_dict(dict): This is the dict between file format and sap document type name
        """
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, UPLOAD_ATTACHMENT_DOCUMENT_TYPES_OVERVIEW_CSS_SELECTOR)))
        target_document_description_list = [item.upper() for item in target_document_type_dict[file_format]]
        upload_document_types = self.browser.find_elements(By.CSS_SELECTOR,
                                                           UPLOAD_ATTACHMENT_DOCUMENT_TYPES_CHOICES_CSS_SELECTOR)
        for upload_document_type in upload_document_types:
            if upload_document_type.text.strip().upper() in target_document_description_list:
                ActionChains(self.browser).double_click(upload_document_type).perform()
                ActionChains(self.browser).reset_actions()
                sleep(2)
                break

        self.wait_file_upload_confirmation_dialog()
        self.wait_com_window_pop_up(window_class, window_name)
        self.process_file_upload_com_window(window_class, window_name, file_path)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, FILE_UPLOAD_INPUT_CSS_SELECTOR)))
        sleep(1)
        self.click_or_input_by_css_selector(
            FILE_UPLOAD_CONTINUE_CSS_SELECTOR, 'click')
        self.wait.until(EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, FILE_UPLOAD_CONTINUE_CSS_SELECTOR)))
        self.wait_invisibility_of_loading_window()


class FF5Functions(WebSapCommonFunctions):
    """This class is used to process tasks within T-Code FF.5

    """

    def __init__(self, browser: Firefox, wait: WebDriverWait):
        """This function is used to initial parameters

        Args:
            browser(Firefox): This is the webdriver instance
            wait(WebDriverWait): This is the WebDriverWait instance
        """
        super().__init__()
        self.browser = browser
        self.wait = wait

    def choose_bank_statement_type(self, bank_statement_type_name: str):
        """This function is used to choose bank statement type

        Args:
            bank_statement_type_name(str): This is the name of target bank statement type
        """
        sleep(1)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, DROP_DOWN_ICON_CSS_SELECTOR)))
        sleep(1)
        self.click_or_input_by_css_selector(DROP_DOWN_ICON_CSS_SELECTOR, 'click')
        sleep(1)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, BANK_STATEMENT_LIST_CSS_SELECTOR)))
        sleep(1)
        self.click_or_input_by_css_selector(f"div[data-itemvalue2='{bank_statement_type_name}']", 'click')
        sleep(1)

    def click_statement_file_input_field(self):
        """This function is used to click statement file input field and then click statement file span to pop up upload
        file confirmation dialog

        """
        sleep(1)
        statement_file = self.browser.find_element(By.CSS_SELECTOR, BANK_STATEMENT_FILE_INPUT_CSS_SELECTOR)
        ActionChains(self.browser).click(statement_file).perform()
        ActionChains(self.browser).reset_actions()
        sleep(1)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, BANK_STATEMENT_FILE_SPAN_CSS_SELECTOR)))
        sleep(1)
        self.click_or_input_by_css_selector(BANK_STATEMENT_FILE_SPAN_CSS_SELECTOR, 'click')
