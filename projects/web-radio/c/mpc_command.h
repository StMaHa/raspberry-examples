#ifndef MPC_COMMAND
#define MPC_COMMAND


#define MPC_MAX_TEXT_LENGTH     100
#define MPC_MAX_STATION_COUNT    50
#define MPC_MAX_STDOUT_LINES      3


typedef struct {
    char text[MPC_MAX_TEXT_LENGTH];
} MpcString;

typedef struct {
    MpcString stations[MPC_MAX_STATION_COUNT];
} MpcPlaylist;

typedef struct {
   char station[40];
   char info1[40];
   char info2[40];
   char status[50];
   char attributes[100];
} MpcStation;


int mpc_play_station(int station_idx, MpcStation* station_info);
int mpc_get_playlist(MpcPlaylist* play_list);
int mpc_stop();
int mpc_set_volume(int volume);
int mpc_get_volume();
int mpc_get_info(MpcStation* station_info);

#endif  // MPC_COMMAND
