
#include <stdio.h>
#include <stdint.h>
#include <limits.h>
#include <string.h>
#include <portaudio.h>

#define FPB 256 //frames per buffer
#define FRS 4 //frame size

int main(int argc, char** argv){
	PaStream* stream;
	Pa_Initialize();
	Pa_OpenDefaultStream(&stream,
			0, //no input
			1, //1 output channel
			paInt16,
			44100,
			FPB, //frames per buffer
			NULL,
			NULL	
			);
	Pa_StartStream( stream );
	FILE* file = stdin;
	if(argc > 1){
		file = fopen(argv[1], "r");
	}
	int matched=1;
	int frame_idx;
	char frame[FRS];
	int16_t buffer[FPB*FRS];
	while(matched > 0){
		frame_idx = 0;
		while(frame_idx < FPB){
			matched = fscanf(file, "%x", buffer + frame_idx); 
			frame_idx++;
			if(matched < 1){
				break;
			}
		}
		if(frame_idx < FPB && frame_idx > 0){
			for(;frame_idx<FPB;frame_idx++){
				buffer[frame_idx]=buffer[frame_idx-1]*0.9;
			}
		}
		Pa_WriteStream( stream, buffer, frame_idx );

	}
	Pa_StopStream( stream );
	Pa_CloseStream( stream );
	if(argc > 1){
		fclose(file);
	}

}
