from _typeshed import Incomplete
from virtualitics_sdk.elements.dropdown import Dropdown as Dropdown
from virtualitics_sdk.utils.types import ConnectionType as ConnectionType

class DataSourceDropdown(Dropdown):
    '''Used to configure data source drop down options that have been set up in the Connections tab.    
    :param user_id: str, the user_id of the owner of the connections, usually done via StoreInterface(**flow_metadata).user.
    :param options: List[ConnectionType], a list of ConnectionTypes, for example ConnectionType.mssql.
    :param selected: Optional[List[str]] = None, used if you want a default selection.
    :param include_nulls_visible: bool = True, whether null values will be visible.
    :param include_nulls_value: bool = False, whether to include null values.
    :param title: str = "", the title of the drop-down element.
    :param description: str = "", the description of the drop-down element.
    :param show_title: bool = True, whether to show the title.
    :param show_description: bool = True, whether to show the description.
    :param required: bool = True, whether selecting an item from the dropdown is required to proceed.
    :param label: str = "", the label of the element.
    :param placeholder: str = "" the placeholder of the element.

    **EXAMPLE:**

       .. code-block:: python

           # Imports 
           from virtualitics_sdk.elements.dropdown_data_sources import DataSourceDropdown
           . . .
           # Example usage
           class ExampleStep(Step):
             def run(self, flow_metadata):
               . . . 
               api_key_selection = DataSourceDropdown(user_id=store_interface.user,
                                                          options=[ConnectionType.s3, 
                                                          ConnectionType.other],
                                                          title=\'Select API Credential\')
               
    The above DataSourceDropdown example will be displayed as: 

       .. image:: ../images/dropdown_data_ex.png
          :align: center
    '''
    user_id: Incomplete
    required: Incomplete
    def __init__(self, user_id: str, options: list[ConnectionType], selected: list[str] | None = None, include_nulls_visible: bool = True, include_nulls_value: bool = False, title: str = '', description: str = '', show_title: bool = True, show_description: bool = True, required: bool = True, label: str = '', placeholder: str = '') -> None: ...
    @staticmethod
    def conn2dropdown_str(filter_options, user_id: str): ...
    @staticmethod
    def dropdown_str2conn(user_id: str, connection_str: str): ...
    def get_value(self) -> str | dict: ...
