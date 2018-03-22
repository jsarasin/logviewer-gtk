class MessageColumns:
    """

    """
    columns = []
    def __init__(self):
        self.columns = []
        self.tool_tip_column = None

    def AddColumn(self, key, display_name, data_type, combo_name='', visible=True):
        self.columns.append((key, display_name, data_type, combo_name, visible))

    def GetTooltipColumn(self):
        # TODO: This isn't probably the best place to adjust this, but I'm tired and want to see it
        # This is assuming the view hides combo_names
        return self.tool_tip_column

    def SetTooltipColumn(self, key_for_tooltip):
        tool_tip_column = None

        i = 0
        for n in self.columns:
            key, display_name, data_type, combo_name, visible = n
            if key == key_for_tooltip:
                tool_tip_column = i
                break
            if combo_name == '':
                i = i +1


        if tool_tip_column is None:
            raise Exception("Key name not found")
        self.tool_tip_column = tool_tip_column

    def GetColumns(self):

        if False:
            print ("Columns: ")

            for n in self.columns:
                column_key, column_display_name, column_type, column_combo, column_visible = n

                print ("   %s" % column_key)

        return self.columns
