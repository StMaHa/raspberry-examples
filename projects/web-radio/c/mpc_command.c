#include "mpc_command.h"
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>


/*
 * Private function to call 'mpc' command line tool
 */
void __mpc_command(char* subcmd, MpcString* stdout, int* size) {
    int i = 0;
    char command[20];
    char text[MPC_MAX_TEXT_LENGTH];
    FILE* file = NULL;
    sprintf(command, "mpc %s", subcmd);
    file = popen(command, "r");
    while (fgets(text, MPC_MAX_TEXT_LENGTH, file) != NULL) {
        text[strlen(text)-1] = '\0';  // remove newline
        strcpy(stdout[i].text, text);
        if(i++ >= *size)
            break;
    }
    *size = i;
    pclose(file);
}

/*
 * Private function to retrieve station information returned by 'mpc'
 */
void __get_station_info(MpcString *info_raw, MpcStation *info) {
    char *value;
    int station_set = 0;
    value = info->station;
    int idx = 0;
    // parse first line of stdout
    for(int i = 0; i < strlen(info_raw[0].text); i++) {
        char letter = info_raw[0].text[i];
        // ignore leading white spaces
        if((letter == ' ') && (idx <= 1))
            continue;
        // first limiter for second element
        if((!station_set) && (letter == ':')) {
            station_set = 1;
            value = info->info1;
            idx = 0;
            continue;
        }
        // second limiter for third element
        if(station_set && ((letter == '-') || (letter == ':'))) {
            value = info->info2;
            idx = 0;
            continue;
        }
        // end of parsing, exit after third element
        if(station_set && ((letter == '|') || (letter == '*'))) {
            break;
        }
        value[idx++] = letter;
    }
    strcpy(info->status, info_raw[1].text);
    strcpy(info->attributes, info_raw[2].text);
}

/*
 * Public function to play station by calling 'mpc play x'
 */
int mpc_play_station(int station_idx, MpcStation* station_info) {
    int size = MPC_MAX_STDOUT_LINES;
    char subcmd[10];
    MpcString info[size];
    // initialice memory to '0'
    memset(info, 0, sizeof(MpcString) * size);
    memset(station_info, 0, sizeof(MpcStation));
    // call 'mpc play x'
    sprintf(subcmd, "play %d%", station_idx);
    __mpc_command(subcmd, info, &size);
    // extract needed data from stdout
    if (size == MPC_MAX_STDOUT_LINES) {
        __get_station_info(info, station_info);
    } else
        size = 0;
    // returns amount of accessed stdout lines
   return size;
}

/*
 * Public function to extract mpc playlist
 */
int mpc_get_playlist(MpcPlaylist* play_list) {
    int count = MPC_MAX_STATION_COUNT;
    char *station = NULL;
    // initialice memory to '0'
    memset(play_list, 0, sizeof(MpcPlaylist));
    __mpc_command("playlist", play_list->stations, &count);
    for(int station_no = 0; station_no < count; station_no++) {
        station = play_list->stations[station_no].text;
        for(int i = 0; i < strlen(station); i++) {
            // name of station completed
            if(station[i] == ':') {
                // terminate string when ':' has been detected
                station[i] = 0;
                break;
            }
        }
    }
    // returns amount of available stations
   return count;
}

/*
 * Public function to turn off web radio by calling 'mpc stop'
 */
int mpc_stop() {
    int result = 0;
    int size = MPC_MAX_STDOUT_LINES;
    MpcString info[size];
    // initialice memory to '0'
    memset(info, 0, sizeof(MpcString) * size);
    // call 'mpc stop'
    __mpc_command("stop", info, &size);
    // check that mpc stop was successfull
    size = MPC_MAX_STDOUT_LINES;
    memset(info, 0, sizeof(MpcString) * size);
    __mpc_command("current", info, &size);
    if(size == 0)  // is success?
        result = 1;
    return result;
}

/*
 * Public function to set volume by calling 'mpc volume x'
 */
int mpc_set_volume(int volume) {
    int size = MPC_MAX_STDOUT_LINES;
    char subcmd[10];
    MpcString info[size];
    // initialice memory to '0'
    memset(info, 0, sizeof(MpcString) * size);
    // call 'mpc volume x'
    sprintf(subcmd, "volume %d%", volume);
    __mpc_command(subcmd, info, &size);
    // returns amount of accessed stdout lines
    return size;
}

/*
 * Public function to retrieve actual volume by calling 'mpc volume'
 */
int mpc_get_volume() {
    int size = MPC_MAX_STDOUT_LINES;
    MpcString info[size];
    int volume = -1;  // returns -1 in case of failure: command failed, no volume number found
    // initialice memory to '0'
    memset(info, 0, sizeof(MpcString) * size);
    // cal 'mpc volume' to retreive data containig actual volume
    __mpc_command("volume", info, &size);
    int digit = 100;  // max 100%
    int line_no = 0;
    // loop through all stdout lines
    while (line_no < size) {
        // find volume information
        if(strstr(info[line_no].text, "volume:") == info[line_no].text) {
            // extract volume value
            for(int i = 0; i < strlen(info[line_no].text) - 1; i++) {
                // value will start after 'volume:' with no, one or two spaces
                if(info[line_no].text[i] == ' ') {
                    digit = digit / 10;
                    continue;
                }
                if((info[line_no].text[i] >= '0') && (info[line_no].text[i] <= '9')) {
                    if (volume < 0) // initialice volume at first hit of valid 
                        volume = 0;
                    volume = volume + (((int)info[line_no].text[i]-48) * digit);
                    digit = digit / 10;
                }
                if(info[line_no].text[i] == '%')
                    break;
            }
            break;
        }
        line_no++;
    }
    // returns actual volume
    return volume;
}

/*
 * Get information from actual station
 */
int mpc_get_info(MpcStation* station_info) {
    int size = MPC_MAX_STDOUT_LINES;
    MpcString info_text[size];
    memset(info_text, 0, sizeof(MpcString) * size);
    memset(station_info, 0, sizeof(MpcStation));
    // call 'mpc current' to retrieve actual information of set radio station
    __mpc_command("current", info_text, &size);
    if (size > 0) {
        __get_station_info(info_text, station_info);
    }
    // returns amount of accessed stdout lines
    return size;
}
