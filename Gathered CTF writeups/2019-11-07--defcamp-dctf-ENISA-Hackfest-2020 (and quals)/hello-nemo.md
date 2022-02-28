### CHALLENGE PROMPT :

We just managed to intercept Cpt. Nemo of the Nautilus submarine. Something's fishy over here...
Download nemo.pcapng and start the investigation.

----------------------------------------------------------------------------------------------------

We are given a network packet capture , *nemo.pcapng* .

Running 
  
  >foremost nemo.pcapng

outputs :

  |foundat=flag.txtUT <br/>
   foundat=flag.txtUT <br/>
 *| <br/>

Foremost seems to have found an interesting file , flag.txt , and it also created a .zip folder located
inside the /output/ directory . The zip folder contains two zip files :*00000061.zip* and *00000062.zip*

Peeking inside *00000061.zip* and *00000062.zip* we find out that they contain the flag.txt found earlier,
however when trying to extract the zip files in order to get to the flag we are met with a prompt asking
us for a password . Let's take a look at the pcap and see if we can find the password .

Looking at the protocol hierarchy statistics , we can get a general overview of the protocols used in the
capture . FTP immediately catches my eye , since protocols like FTP , HTTP , TELNET are unencrypted by
default and can reveal a lot of useful information .

![hierarchypcap](https://user-images.githubusercontent.com/73142671/104407215-c893f980-5569-11eb-87cc-cb40a91cf969.png)

---------------------------------------------------------------------------------------

Here is a small snippet of the FTP traffic , in summary by analyzing some more FTP packets we can tell that 
someone logs in as user through FTP , and uploads flag.zip . Then , they download a file called password.txt . 


![ftp](https://user-images.githubusercontent.com/73142671/104407625-b8c8e500-556a-11eb-8e70-bfef98c13dee.png)

---------------------------------------------------------------------------------------

Continuing forward , lets analyze the TELNET packets . Filtering for TELNET in wireshark , we select whichever
packet , right click it , select follow and then follow TCP stream .

We can tell that someone is poking around in here , running a lot of commands . However , aadysgaugysdihsasdh
doesnt seem to be the password for the .zip files .

![tel1](https://user-images.githubusercontent.com/73142671/104408224-448f4100-556c-11eb-8973-6abd53b0a606.png)

----------------------------------------------------------------------------------------

In this snippet bellow we see that " dgyfogfoewyeowyefowouevftowyefg " is being written to password.txt :

 " ccaatt  dgyfogfoewyeowyefowouevftowyefgdgyfogfoewyeowyefowouevftowyefg  >>  ppaa 
    .ssss	word.txt "
    
![fin89](https://user-images.githubusercontent.com/73142671/104408538-deef8480-556c-11eb-8dd1-4952c8375928.png)


Now unziping 00000061.zip with " dgyfogfoewyeowyefowouevftowyefg " as the password when prompted , we get the flag.

**DCTF{3907879c7744872694209e3ea9d2697508b7a0a464afddb2660de7ed0052d7a7}**

