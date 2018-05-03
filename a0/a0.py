<<<<<<< HEAD
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
from TwitterAPI import TwitterAPI
import configparser



def read_screen_names(filename):
    sobj1=[]
    for line in open(filename):
        sobj1.append(line.rstrip('\n'))
    return sobj1

def get_twitter():
    config = configparser.ConfigParser()
    config.read('twitter.cfg')
    twitter = TwitterAPI(
        config.get('twitter', 'consumer_key'),
        config.get('twitter', 'consumer_secret'),
        config.get('twitter', 'access_token'),
        config.get('twitter', 'access_token_secret'))
    return twitter

def robust_request(twitter, resource, params, max_tries=5):
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)

def get_users(twitter, screen_names):
    request = robust_request(twitter, 'users/lookup', {'screen_name': screen_names})
    user =[r for r in request]
    uinfo = [user[i] for i in range(0,4)]
    return uinfo



def get_friends(twitter, screen_names):
    request = robust_request(twitter,'friends/ids', {'screen_name': screen_names,'count': 5000})
    res=[r for r in request]
    return sorted(res)



def add_all_friends(twitter, users):
    

    for x in range(0,len(users)):
        z=get_friends(twitter,users[x]['screen_name'])
        users[x]['friends']=z






def print_num_friends(users):
    
    for x in range(0,len(users)):
       print(users[x]['screen_name'] +':' + str(users[x]['friends_count']))
    


def count_friends(users):
    cnt1 = Counter()
    for i in range(len(users)):
        for friend in users[i]['friends']:
            cnt1[friend] +=1
    return cnt1





def friend_overlap(users):
   
    
    for i in range(0,4):
        for j in range(1,4):
            if i!=j:
               list= set(users[i]['friends'])&set(users[j]['friends'])
               print([users[i]['screen_name'],users[j]['screen_name'],len(list)])
            else:
                return j+1
        
    

    




def followed_by_hillary_and_donald(users, twitter):
    """
    Find and return the screen_name of the one Twitter user followed by both Hillary
    Clinton and Donald Trump. You will need to use the TwitterAPI to convert
    the Twitter ID to a screen_name. See:
    https://dev.twitter.com/rest/reference/get/users/lookup

    Params:
        users.....The list of user dicts
        twitter...The Twitter API object
    Returns:
        A string containing the single Twitter screen_name of the user
        that is followed by both Hillary Clinton and Donald Trump.
    """
    rec=set(users[2]['friends'])& set(users[3]['friends'])
    req=twitter.request('users/lookup',{'user_id': rec})
    us =[r for r in req]
    rec_name=us[0]['screen_name']
    return rec_name

def create_graph(users, friend_counts):
    """ Create a networkx undirected Graph, adding each candidate and friend
        as a node.  Note: while all candidates should be added to the graph,
        only add friends to the graph if they are followed by more than one
        candidate. (This is to reduce clutter.)

        Each candidate in the Graph will be represented by their screen_name,
        while each friend will be represented by their user id.

    Args:
      users...........The list of user dicts.
      friend_counts...The Counter dict mapping each friend to the number of candidates that follow them.
    Returns:
      A networkx Graph
    """

    gr=nx.Graph()
    for i in users['screen_name']:
        gr.add_node(i)
        for every in users[i]:
            if friend_counts[every]>1:
                gr.add_node(every)
                gr.add_edge(i,every)
    return gr

   
        









def draw_network(graph, users, filename):
    """
    Draw the network to a file. Only label the candidate nodes; the friend
    nodes should have no labels (to reduce clutter).

    Methods you'll need include networkx.draw_networkx, plt.figure, and plt.savefig.

    Your figure does not have to look exactly the same as mine, but try to
    make it look presentable.
    """
    labels = {n: n if n in users or friend_counts[n]>3 else ''for n in gr.nodes()}
    plt.figure(figsize=(12,12))
    nx.draw_networkx(gr,node_color='r',
            labels=labels,alpha=.5,width=.1,
            node_size=100)
    plt.axis("off")
    plt.show()

def main():
    """ Main method. You should not modify this. """
    twitter = get_twitter()
    screen_names = read_screen_names('C:\\Users\\DELL\\PycharmProjects\\untitled2\\candidates.txt')
    print('Established Twitter connection.')
    print('Read screen names: %s' % screen_names)
    users = sorted(get_users(twitter, screen_names), key=lambda x: x['screen_name'])
    print('found %d users with screen_names %s' %
          (len(users), str([u['screen_name'] for u in users])))
    add_all_friends(twitter, users)
    print('Friends per candidate:')
    print_num_friends(users)
    friend_counts = count_friends(users)
    print('Most common friends:\n%s' % str(friend_counts.most_common(5)))
    print('Friend Overlap:\n%s' % str(friend_overlap(users)))
    print('User followed by Hillary and Donald: %s' % followed_by_hillary_and_donald(users, twitter))

    graph = create_graph(users, friend_counts)
    print('graph has %s nodes and %s edges' % (len(graph.nodes()), len(graph.edges())))
    draw_network(graph, users, 'network.png')
    print('network drawn to network.png')


if __name__ == '__main__':
    main()

# That's it for now! This should give you an introduction to some of the data we'll study in this course.
=======

