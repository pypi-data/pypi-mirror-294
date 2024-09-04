
def pan_validation(pan):
    print("PAN should be in string format")
    if len(pan) == 10:
        if pan[0:5].isalpha():
            if pan[5:9].isdigit():
                if pan[9].isalpha():
                    print("The given pan {} is valid".format(pan))
                else:
                    print("The last position  should  be char")   
                        
            else:
                print("Should be 6th to 9th position are numbers")
            
        else:
            print("The range of 1st 5 chars should be alpha")
    else:
        print("The pan {} should be 10 digits".format(pan))



