
#include <unistd.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>


#define MPC_MAX_TEXT_LENGTH     100
#define MPC_MAX_STATION_COUNT    50
#define MPC_MAX_INFO_SIZE         3


typedef struct {
    char text[MPC_MAX_TEXT_LENGTH];
} MpcString;

typedef struct {
    MpcString stations[MPC_MAX_STATION_COUNT];
} MpcPlaylist;

typedef struct {
   char station[40];
   char interpret[40];
   char title[40];
   char status[50];
   char attributes[100];
} MpcStation;

void mpc_command(char* subcmd, MpcString* stdout, int* size) {
    int i = 0;
    char command[20];
    char text[MPC_MAX_TEXT_LENGTH];
    FILE* file = NULL;
    sprintf(command, "mpc %s", subcmd);
    file = popen(command, "r");
    memset(stdout, 0, sizeof(*stdout));
    while (fgets(text, MPC_MAX_TEXT_LENGTH, file) != NULL) {
        strcpy(stdout[i].text, text);
        if(i++ >= *size)
            break;
    }
    *size = i;
    pclose(file);
}

void __get_station_info(MpcString *info_raw, MpcStation *info) {
    memset(info, 0, sizeof(*info));
    char *value;
    value = info->station;
    int idx = 0;
    for(int i = 0; i < strlen(info_raw[0].text); i++) {
        char letter = info_raw[0].text[i];
        if((letter == ' ') && (idx <= 1))
            continue;
        if(letter == ':') {
            value = info->interpret;
            idx = 0;
            continue;
        }
        if(letter == '-') {
            value = info->title;
            idx = 0;
            continue;
        }
        if(letter == '|') {
            break;
        }
        value[idx++] = letter;
    }
    strcpy(info->status, info_raw[1].text);
    strcpy(info->attributes, info_raw[2].text);
}

int mpc_play_station(int station_idx, MpcStation* station_info) {
    int size = MPC_MAX_INFO_SIZE;
    char subcmd[10];
    MpcString info[size];
    sprintf(subcmd, "play %d%", station_idx);
    mpc_command(subcmd, info, &size);
    if (size == MPC_MAX_INFO_SIZE) {
        __get_station_info(info, station_info);
    }
    return size;
}

int mpc_get_playlist(MpcPlaylist* play_list) {
    int size = MPC_MAX_STATION_COUNT;
    mpc_command("playlist", play_list->stations, &size);
    return size;
}

int mpc_set_volume(int volume) {
    int size = MPC_MAX_INFO_SIZE;
    char subcmd[10];
    MpcString info[size];
    sprintf(subcmd, "volume %d%", volume);
    mpc_command(subcmd, info, &size);
    return size;
}

int mpc_get_volume() {
    int size = MPC_MAX_INFO_SIZE;
    MpcString info[size];
    int volume = -1;  // returns -1 in case of failure: command failed, no volume number found
    int digit = 1;
    mpc_command("volume", info, &size);
    if (size > 0) {
        int i = strlen(info[0].text) - 1;

        while ( i > 0) {
            if((info[0].text[i] >= '0') && (info[0].text[i] <= '9')) {
                if (volume < 0)
                    volume = 0;
                volume = volume + (((int)info[0].text[i]-48) * digit);
                digit = digit * 10;
            }
            i--;
        }
    }
    return volume;
}

int mpc_get_info(MpcStation* station_info) {
    int size = MPC_MAX_INFO_SIZE;
    MpcString info_text[size];
    mpc_command("current", info_text, &size);
    if (size > 0) {
        __get_station_info(info_text, station_info);
    }
    return size;
}

void main() {
    MpcPlaylist playlist;
    printf("Get playlist...\n");
    int station_count = mpc_get_playlist(&playlist);
    printf("Found %d stations.\n", station_count);
    for(int i = 0; i < station_count; i++)
        printf("%s", playlist.stations[i].text);
    printf("\n");

    MpcStation output;
    mpc_get_info(&output);
    printf("ST %s\n", output.station);
    printf("IN %s\n", output.interpret);
    printf("TI %s\n", output.title);
    printf("ST %s\n", output.status);
    printf("AT %s\n", output.attributes);

    mpc_play_station(6, &output); // Rock Antenne
    printf("ST %s\n", output.station);
    printf("IN %s\n", output.interpret);
    printf("TI %s\n", output.title);
    printf("ST %s\n", output.status);
    printf("AT %s\n", output.attributes);

    int result = mpc_set_volume(50);  // Volume on 50%
    printf("Set volume: %d\n", result);

    int vol = mpc_get_volume();
    printf("Volume %d\n", vol);
}
