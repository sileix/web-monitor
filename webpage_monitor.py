import time, urllib2, pygame

# monitor url
url = 'http://www.shopbop.com/karen-walker/br/v=1/2534374302162611.htm'
# interval of monitor
interval = 3
# alarm audio
alarm_file = 'door_bell.wav'
# repeat times of alarm audio
repeat_time = 3
# text before monitor target
target_flag = '<div id="searchResultCount">'
# length of target text
target_length = 2
# tolerance of target's change (only available when target are integer or float)
target_tolerance = 1


def play_alarm():
    ''' play the given alarm audio file '''
    pygame.mixer.init()
    pygame.mixer.music.load(alarm_file)
    pygame.mixer.music.play(repeat_time, 0.0)

def monitor_target(page):
    ''' return the target value '''
    page = str(page)
    index = page.find(target_flag)
    if index != -1:
        target_pos = index + len(target_flag)
        return page[target_pos:target_pos + target_length]

def equal(origin_value, new_value):
    ''' return whether origin_value and new_value are equal '''
    if (isinstance(origin_value, int) and isinstance(new_value, int)) \
    or (isinstance(origin_value, float) and isinstance(new_value, float)):
        if abs(float(origin_value) - float(new_value)) <= target_tolerance:
            return True
        else:
            return False
    else:
        return origin_value == new_value

def monitor():
    ''' monitor process '''
    print 'Load url...'
    base_page = urllib2.urlopen(url).read()

    print 'Finding target...'
    origin_value = monitor_target(base_page)

    print 'Start monitor...'
    while True:
        new_page = urllib2.urlopen(url).read()
        new_value = monitor_target(new_page)
        if equal(origin_value, new_value):
            print 'Nothing changed -' + time.strftime('%H:%M:%S')
            time.sleep(interval)
        else:
            print 'Target changed! -' + time.strftime('%H:%M:%S')
            print origin_value + ' -> ' + new_value
            play_alarm()
            if str(raw_input('Keep on monitoring? y/n: ')) == 'y':
                origin_value = new_value
            else:
                exit(0)


if __name__ == "__main__":
        monitor()




