# image-to-cv

## Original Idea
An idea I originally came up with when a photographer friend reached out to me several years ago and wanted to do some sort of musical/photography collaboration and performance. When my friend approached me, I had recently become obsessed with creating generative music, so I opted to use their photography to be the modulation source for several electronic instruments. 

The original proof of concept used VCV Rack to analyze an image and convert each pixel of the image to a CV value (or multiple CV values), which then eventually controlled different voices and modulations. Unfortunately, my friend experienced several life changing events near the completion of the POC and the collobaration was abandoned. I archived the VCV Rack implemntation of the idea.

During the winter months on the weekends, I typically tinker with micro electronics and build modular synthesizer kits in my free time as it's too cold to do anything outdoors. I find it peaceful and provides stress relief. Plus modular synthesizer kits are cheaper than Lego kits (another activity I discovered that helps me unwind). I began to tinker with the arduino nano to see what it could do. And the more and more I tinkered with it, I realized it could easily be used as a component for a synthesizer module. Then I quickly learned that modular synth designers have been using the Nano for years... Regardless, my mind start to race with the possibilites now that I began to understand the Nano more and more.

One night, during a bout of insomnia, I was thinking about my friend and the project we worked on together and I remembered the POC we worked on. And I began thinking of ways to convert that idea in VCV rack into a physical module. Eventually I gave up sleeping that evening and began sketching out the idea on a piece of paper, making notes and ordered a handful of various electronic compoments that I'd need. 

The following Sunday, I began breadboarding the idea using the Nano, several DACs (MCP4725) and an SD card reader. 

At this point, the core of the POC is there, though there is quite a ways to go. As of today, there is no way to alter settings beyond the code on the Nano. My original sketch of the module includes multiple ways in which to interact with the settings and how an image affects the CV values. The Nano is not powerful enough to analyze an image for pixel values, so currently it simply reads a text/csv file that contains the RGB values for each pixel on a separate line. And most of all, I have no idea how I'm going to bundle everything together into a size that's compatible with the Eurorack format. But what kind of hobby project would it be if I ever finished it :)

Sketches of the original idea are in Notes/ folder; I figure it's best to have a backup just in case I need to reference my original vision.

The code in it's current state is in no way optimized and my C has become rusty after years of not coding in it. The code itself is definately a WIP.

I know this isn't a typical ReadMe, but I figure this is my own little hobby project that's a WIP, so if I ever do complete it, I'll rewrite all of this into a step-by-step guide on how to build it. 

But if you happen to stumble across this repository and find it somewhat interesting of an idea and want to chat about it or really anything to do with DIY synthesizers, please reach out to me.



## Feature Ideas

* Could write back out to the SD card the RGB values that were transformed by the module's settings. For example, if the **red** channel was attenuated to 3 o'clock and the **green** channel attenuation was set at noon and the **blue** channel was set at 9PM, perform the attentuation calculation on the original RGB values and write them back out to the SD card in a subfolder labeled something like  `[YYYY-MM-DD]-[original-input-filename]-performance.csv`. Could provide a way for the user to automatically open up the latest performance.csv (or oldest, whatever really) when the module reaches the end of the original file (rather than simply looping back again from the beginning of the original file). Realistically, over time, if one begins with an image and _only_ uses the most recent performance file, the attenuation will be filled up with lines of either ```255,255,255``` or ```0,0,0```, but that's to be expected.

