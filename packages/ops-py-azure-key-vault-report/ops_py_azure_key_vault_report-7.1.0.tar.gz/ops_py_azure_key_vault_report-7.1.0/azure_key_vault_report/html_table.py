#!/usr/bin/env python


########################################################################################################################


class HTMLTable(object):
    """Creates a html table based on provides list of header elements and row elements.

    Attributes
    ----------
    table_header : list
        A list of header elements - the heading of each column.
    html_table : str
        The html table

    Methods
    -------
    init_html_table(table_header)
        Generates the first part of the table - the header
    add_html_row(*args)
        Add each provides arguments as column items and finally appends the complete row to the table.
    get_table(*args)
        Finalize and returns the table.
    """
    def __init__(self, table_header):
        """
        Parameters
        ----------
        table_header : list
            A list of header elements - the heading of each column.
        """

        grey = "<td style='background-color: Grey; color: White; font-weight:bold'>"
        purple = "<td style='background-color: Purple; color: White; font-weight:bold'>"
        yellow = "<td style='background-color: Yellow; color: Black; font-weight:bold'>"
        red = "<td style='background-color: Red; color: White; font-weight:bold'>"

        self.table_header = table_header
        self.html_table = ""

        self.disabled_txt = "Disabled"
        self.will_expire_txt = "Will expire"
        self.expired_txt = "Expired"
        self.has_no_expiration = "Has no expiration"
        self.error_txt = "ERROR"

        self.alert_styles = {
            self.disabled_txt: grey,
            self.will_expire_txt: yellow,
            self.expired_txt: red,
            self.has_no_expiration: purple,
            self.error_txt: red
        }

    def init_html_table(self):
        """generates a html table to be used in json output for MS Teams"""

        self.html_table = f"""<table bordercolor='black' border='2'>
    <thead>
    <tr style='background-color: Teal; color: White'>
"""
        for h in self.table_header:
            self.html_table += f"        <th>{h}</th>\n"

        self.html_table += """
    </tr>
    </thead>
    <tbody>
    """

    def add_html_row(self, *args):
        """adds the table rows to the html table

        expected row elements:
            record_name, record_type, vault_name, updated, expires, comment

        Parameters
        ----------
        args : str
            The items which will be added to the current row.
        """

        if not self.html_table:
            return

        html_row = "<tr>"
        for arg in args:
            td = "<td>"
            if arg.startswith(self.disabled_txt):
                td = self.alert_styles.get(self.disabled_txt)
            if arg.startswith(self.will_expire_txt):
                td = self.alert_styles.get(self.will_expire_txt)
            if arg.startswith(self.expired_txt):
                td = self.alert_styles.get(self.expired_txt)
            if arg.startswith(self.has_no_expiration):
                td = self.alert_styles.get(self.has_no_expiration)
            if arg.startswith(self.error_txt):
                td = self.alert_styles.get(self.error_txt)
            arg = arg.replace(". ", "<br>").replace(" (", "<br>(")
            html_row += f"{td}{arg}</td>"
        html_row += "</tr>"

        self.html_table += html_row

    def get_table(self):
        """adding closing html tags and remove plural in days when it should not be used

        Returns
        -------
        html_table : str
            The finalized table.
        """

        if self.html_table:
            self.html_table += "</tbody></table>"
            self.html_table = self.html_table.replace(" 1 days", " 1 day").replace("\n", "")
        return self.html_table
