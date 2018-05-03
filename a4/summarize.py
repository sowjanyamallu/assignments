import pickle
def main():
    tweets = pickle.load(open('tweet_64.pkl', 'rb'))
    f2 = pickle.load(open('clstropt.pkl', 'rb'))
    i = 0
    lt = []
    g = []
    for i in range(len(f2)):
        for j in range(0, 2):
            lt.append(len(f2[i][j]))
    for p in tweets:
        g.append(p['text'])
    hscreenname = []
    for j in tweets:
        if j['user']['protected'] == False:
            hscreenname.append(j['user']['screen_name'])
    kc = pickle.load(open('opclf.pkl', 'rb'))

    f = open('summary.txt', 'w+')
    f.write("NUMBER OF USERS COLLECTED : %d\n" % (len(set(hscreenname))))
    f.write("NUMBER OF MESSAGES COLLECTED : %d\n" % (len(g)))
    f.write("NUMBER OF COMMUNITIES DISCOVERED : %d\n" % (len(lt)))
    f.write("AVERAGE NUMBER OF USERS PER COMMUNITY : %d\n" % (sum(lt) / len(lt)))
    f.write("NUMBER OF INSTANCES PER CLASS FOUND :\nPOSITIVES :%d\nNEGATIVES :%d\n" % (kc[0], kc[1]))
    f.write("ONE EXAMPLE FROM EACH CLASS :\nInstance for positive tweet:\n")
    for item in kc[2]:
        f.write("TWEET %s\n" % item[0])
        f.write("positive value:%d\n" % item[1])
        f.write("negative value:%d\n" % item[2])

    f.write("\nInstance for negative tweet:\n")
    for item1 in kc[3]:
        f.write("TWEET:%s\n" % item1[0])
        f.write("positive value:%d\n" % item1[1])
        f.write("negative value:%d\n" % item1[2])

if __name__ == '__main__':
    main()




