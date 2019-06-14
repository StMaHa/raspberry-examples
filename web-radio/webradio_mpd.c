// sudo apt install mpc mpd
// sudo apt install libmpdclient-dev

#include <mpd/client.h>
#include <mpd/status.h>
#include <mpd/entity.h>
#include <mpd/search.h>
#include <mpd/tag.h>
#include <mpd/message.h>
#include <mpd/connection.h>

#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>


void main() {
    struct mpd_connection *mpd;
    struct mpd_song *station;

    mpd = mpd_connection_new(NULL, 0, 30000);  // default settings

    mpd_run_play_pos(mpd, 5);     // Rock Antenne
    mpd_run_set_volume(mpd, 50);  // Volume on 50%

    // Get information from radio station
    mpd_send_current_song(mpd);
    if ((station = mpd_recv_song(mpd)) != NULL) {
        printf("uri  : %s\n", mpd_song_get_uri(station));
        printf("title: %s\n", mpd_song_get_tag(station, MPD_TAG_TITLE, 0));
        printf("name : %s\n", mpd_song_get_tag(station, MPD_TAG_NAME, 0));
	printf("pos  : %u\n", mpd_song_get_pos(station));
        mpd_song_free(station);
    }
}
