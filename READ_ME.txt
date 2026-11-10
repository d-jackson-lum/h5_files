Program to be able to browse and plot data channels from .h5 files

After browsing, the program will read all the data channels in the file

Then you can select a slice from that channel

Time is set on the left side of the panel. You can choose milliseconds, seconds, or minutes
	- The time value can be typed in, but you must press the up/down arrows for the program to update the global variables for start and end time

Fitting options are listed to the right
	- The raw data will always be plotted. A histogram of data is also plotted
	- You can choose to fit a gaussian curve to the histogram. If the fit fails, the code should still run and just not plot the fit
		- Fitting parameters are automatically determined by some statistical model
			- ## based on Freedman-Diaconis rule for data spread
	- You can choose to plot the FFT of the data
	- You can choose to fit a Lorentzian to the FFT. If this option is selected, it automatically selects plot FFT as well
	