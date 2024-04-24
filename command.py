
class Command():
    """
    This class holds information about a command that was issued by the user.
    A command currently consists of two strings: a command word and a second
    word (for example, if the command was "take map", then the two strings
    obviously are "take" and "map").
 
    The way this is used is: Commands are already checked for being valid
    command words. If the user entered an invalid command (a word that is not
    known) then the command word is <None>.
 
    If the command had only one word, then the second word is <None>.
    """

    def __init__( self, first_word, second_word, third_word):
        """ Create a command object. First and second word must be supplied, but
        either one (or both) can be None.
     
        Parameters
        ----------
        first_word: string
            The first word of the command. None if the command was not recognised.
        second_word: string
            The second word of the command.
        """
        self.__command_word = first_word
        self.__second_word = second_word
        self.__third_word = third_word
    
    
    def get_command_word(self):
        """ Return the command word (the first word) of this command. If the
        command was not understood, the result is None.
        
        Returns the command word.
        """
        return self.__command_word

    def get_second_word(self):
        """ Returns the second word of this command. Returns None if there was no second word. """
        return self.__second_word

    def get_third_word(self):
        """ Returns the third word of this command. Returns None if there was no third word. """
        return self.__third_word

    def is_unknown(self):
        """ Returns true if this command was not understood. """
        return (self.__command_word == None)          # None is a special Python value that says the variable contains nothing

    def has_second_word(self):
        """ Returns true if the command has a second word. """
        return (self.__second_word != None)           # None is a special Python value that says the variable contains nothing

    def has_third_word(self):
        """ Returns true if the command has a third word. """
        return (self.__third_word != None)           # None is a special Python value that says the variable contains nothing
