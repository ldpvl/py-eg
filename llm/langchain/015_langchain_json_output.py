from langchain_community.llms import Ollama

text = """
How to Upgrade to an SSD
If you've noticed problems with your computer starting up slowly, taking a long time to load programs and movies, or if you're tired of the upkeep of a hard disk drive, defragmenting and being careful not to bump it while it's running, it might be time to upgrade to a solid state drive.

SSDs start up more quickly and load games, applications, and movies faster. They're also more durable, use less energy, and produce less heat than an HDD.

Upgrading to a solid state drive is not hard. Use the Crucial® Advisor™ tool or System Scanner tool to determine the SSD to order, then follow the instructions below to install your drive in a Microsoft® Windows® computer. For instructions on how to install an SSD in a Mac®, click here.

How to install an SSD
You can watch this video of the steps or read below for instructions on how to install a solid state drive.


Precautions
Static electricity can damage the components in your system. To protect your system’s components from static damage during the installation process, touch any of the unpainted metal surfaces on your computer’s frame or wear an ESD wrist strap before touching or handling internal components. Either method will safely discharge static electricity that’s naturally present in your body.
To protect your new SSD, do not touch the connectors on the drive.
Do not open the SSD. Doing so will void your warranty.
Be sure to move any data you want from your existing drive to the new drive before you install the new drive.
Installation steps
1.    Make sure you’re working in a static-safe environment

 Remove any plastic bags or papers from your work space.

Gather supplies to install your solid state drive.
2.    Gather supplies

·         2.5-inch Crucial® SSD

·         Screwdriver

·         Your computer’s owner’s manual (which will specify the type of screwdriver you need)

3.    Shut down your system

When your system has been powered off, unplug the power cable.

4.    Hold down the power button for 5 seconds to discharge residual electricity

5.    Open the computer case
Refer to your system’s owner’s manual for how to do this.

6.    Ground yourself by touching an unpainted metal surface

This is an extra safeguard that protects your drive and components from static damage during the installation process.

7.    Locate the storage bay

Refer to your owner’s manual for the exact location and note the size of the bays.

Some storage bays and existing hard drives are significantly larger than a standard size SSD. If this is the case in your system, you’ll need a 2.5-inch to 3.5-inch converter to make the SSD fit snugly. Remove your old drive and disconnect any cables and brackets attached to it.

Locate the storage bay to install the solid state drive.
8.    Plug the SSD into your system

 Don’t force the connection – it should plug in easily and fit snugly.

Don't for the connection when installing your solid state drive. 
To install the SSD as a secondary drive (not your primary or boot drive), use a SATA cable and attach one end of the cable to the SATA connector on your motherboard. Attach the other end of the SATA cable to your Crucial SSD. Then, use an available SATA power cable coming from your system’s power supply and connect the cable to your Crucial SSD. For either type of install, consult your owner’s manual for how to remove an existing drive (if necessary), and how to handle the cables.

9.    Reassemble your computer

10.  Power on your computer
You will notice faster boot-up times and loading, less heat and power consumption, and an overall improvement in performance.
"""

prompt = f"""\
Summarize the following text and provide output in JSON format with the keys: "Problem Title", "Problem Description", 
"Solution Steps", "Problem Difficulty"

In the output, just include the JSON and no other plain text such as "Here is the output".

In the JSON output, stylize the text values as markdown if possible.

Text: "{text}"

Output:
{{
    "Problem Title": "",
    "Problem Description": "",
    "Solution Steps": "",
    "Problem Difficulty": ""
}}
"""

llm = Ollama(model="llama3")
res = llm.invoke(prompt)
print(res)