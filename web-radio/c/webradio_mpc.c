#include "mpc_command.h"
#include <stdio.h>
#include <unistd.h>


void main() {
    MpcPlaylist playlist;
    printf("Get playlist...\n");
    int station_count = mpc_get_playlist(&playlist);
    printf("Found %d stations.\n", station_count);
    for(int i = 0; i < station_count; i++)
        printf("%d. %s\n", i + 1, playlist.stations[i].text);
    printf("\n");

    MpcStation output;

    // loop through play list
    for(int i = 0; i < station_count; i++) {
        mpc_play_station(i + 1, &output);
        printf("%d. %s\n", i + 1, playlist.stations[i].text);

        printf("Play station:\n");
        printf("STATION    %s\n", output.station);
        printf("INFO1      %s\n", output.info1);
        printf("INFO2      %s\n", output.info2);
        printf("STATUS     %s\n", output.status);
        printf("ATTRIBUTES %s\n", output.attributes);
        printf("\n");

        mpc_get_info(&output);
        printf("Station information:\n");
        printf("STATION    %s\n", output.station);
        printf("INFO1      %s\n", output.info1);
        printf("INFO2      %s\n", output.info2);
        printf("STATUS     %s\n", output.status);
        printf("ATTRIBUTES %s\n", output.attributes);
        printf("\n");

        int result = mpc_set_volume(50);  // Volume on 50%
        printf("Set volume: %d\n", result);
        printf("\n");

        int vol = mpc_get_volume();
        printf("Volume %d\n", vol);
        printf("\n");

        sleep(5);
    }
    mpc_stop();
    printf("Stop\n");
}
