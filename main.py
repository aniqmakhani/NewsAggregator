import MySQLdb
from crawler import *


if __name__ == '__main__':
    

    crawl = crawler()
    
    rep = 'Y'
    while rep == 'y' or rep == 'Y':
        print ""
        print "-----------------------------------------------------------------------------"
        print "1. Add New Website"
        print "2. Delete Website"
        print "3. Parse News (Just for Demo)"
        print "4. Parse All News from existing xml(s)"
        print "-----------------------------------------------------------------------------"

        choice = int(raw_input("\t\t\t\tEnter Your Choice\n-----------------------------------------------------------------------------\n"))
        print "-----------------------------------------------------------------------------"
        if choice == 1:
            
            link = raw_input('\t\t\t\tEnter a link\n-----------------------------------------------------------------------------\n')
            crawl.add_web(link)
            
        elif choice == 2:
            link = raw_input('\t\t\t\tEnter a link\n-----------------------------------------------------------------------------\n')
            crawl.delete_web(link)

        elif choice == 3:
            link = raw_input('\t\t\t\tEnter a link\n-----------------------------------------------------------------------------\n')
            crawl.parse_one(link)

        elif choice == 4:
            crawl.parse_all()
        else:
            print "Bad Choice"

        rep = raw_input("You Want to continue? (Y/N)")

print ""
print ""
print "-----------------------------------------------------------------------------"
print "\t\t\tThanks for using our crawler"
print "\t\t\t\tGoodbye :-)"
print "-----------------------------------------------------------------------------"
