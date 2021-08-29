
# Lenschecker

The problem is we want to provide the best outcome for the patient. But the other problem is we need to ensure we can make the lens for the patient.

It is embarrasing when we promise to make up glasses for a patient but then it ends up not being possible with the current constraints. The only alternative is a more expensive option or a very angry patient or worse, a very angry boss!

The moral is getting lenses into frames seems like an simple ordeal. Pick a frame get lenses to help you see. Turns out it's a bit more complicated than that. There are a few rules involves as we will discover.

## Some Definitions

For those of you who have no optics background. Here are some definition, albeit quite brief!

**Stock lens** - A stock lens is a pre-grinded lens that can be made quickly and are cheaper, but there are certain constraints.

**Grind lens** - This is a specialised lens, more expensive, but less limitations

**Single Vision Distance/Reading** - These are lenses the focus only for distance or reading.

**Progressives (Progresive Additional Lenses)** - These are lenses that allow focus for reading and distance at the same time

**Occupational** - This is a more speicalised form of progressive, designed for work use.

**Bifocals/Trifocals** - These lenses also allow multiple focus, but the focus points are in a segment.

**Transitions(TM)** - Generically known as photochromatic lenses, this type of lens darkens whne exposed to UV light from the sun.

**Standard Anti-reflection Coating** - This is a coating that reduces reflections of the lens surface.

***Blue Anti-reflection Coating** - This is a special type of anti-reflective coating that cuts down blue light.

## The current workflow

What we currently do, all manually:
1. Determine what the patient needs (e.g. Single vision distane lens, or a progressive with blue light protection, transitions, clip-ons, and X-ray vision... I'm kidding about the X-ray vision).
	a. If the patients wants Single Vision then we need to be careful when looking at Stock vs Grind option
2. Based on the individual's prescription we determine the index.
	- Common power ranges
	- TODO - makes common power range
	- Semi-rimless and Rimless cannot have 1.5 index and need a tougher index.
3. Ensure the addon don't exclude any options 
	a. Firstly, we will need to check if any addons exclude Stock lens:
		- No Blue AR
		- TODO No Transitions on certain index
		- Prisms
	b. Determine if the prescription falls within the allowable range
4. If the lenses is a stock, ensure if the Minimum Blank Size constrains to the blank size of hte lens.

## The aim

We want this: 
Patient wants --> LensChecker --> Validate if patient's needs can be met.

Turn what we manually do into a computer program!
