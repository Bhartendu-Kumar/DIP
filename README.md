
<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url] 
[![LinkedIn][linkedin-shield]][linkedin-url]
-->
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]




<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Bhartendu-Kumar/DIP">
    <img src="images/logo.gif" alt="Logo" width="80" height="80">
  </a>
  
  
 
<h3 align="center">Exploring Blind Preprocessing to Improve Viola-Jones</h3>

  <p align="center">
    We are interested in studying the impact of applying various pre-processing methods on the detection efficiency of Viola-Jones detector. The pre-processing has to be blind so to be applied in all scenarios and still we do get better performance. 
    <br />
    <a href="https://github.com/Bhartendu-Kumar/DIP"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Bhartendu-Kumar/DIP">View Demo</a>
    ·
    <a href="https://github.com/Bhartendu-Kumar/DIP">Report Bug</a>
    ·
    <a href="https://github.com/Bhartendu-Kumar/DIP">Request Feature</a>
  </p>
</div>


   
    





<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#Introduction">Introduction 
</a>
      <ul>
        <li><a href="#Pre-Processing-Algorithms">Pre-Processing-Algorithms</a></li>
        <li><a href="#Data-Sets">Data-Sets</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


<a id ="Introduction"></a>
<!-- Introduction -->
## Introduction

[![Product Name Screen Shot][product-screenshot]](https://example.com)




Viola-Jones Detector is an object detection Algorithm (which was originally developed for detecting faces. We are trying to increase (possibly ::exclamation:)  the detection efficiency by applying some pre-processing to images. Thus our **GOAL** is to study the impact of difference pre-processing algos to the viola jones detector.

<p align="right">(<a href="#top">back to top</a>)</p>



<a id ="#Pre-Processing-Algorithms"> </a>
### Pre-Processing-Algorithms

----------------------------------------------------------------------------------------
#### I. Lightning Invarient / Intensity Normalization:
* [Retinex Methods](https://github.com/Bhartendu-Kumar/DIP/blob/main/scripts/retinex.py) 

1. SSR (single scale retinex) 
*we want to see if there is good sigma value (gaussian kernel)*
2. MSR (multi scale retinex)
	*to find list of sigmas*
3. Frankle-McCann Retinex
(*in build* : `Adaptive SSR` ) 
* [Non Local Means Methods](https://github.com/Bhartendu-Kumar/DIP/blob/main/scripts/nmbm.py) 
4. NMBM 
*to estimate best patch size , h , patch distance*
* [Normalization Methods](https://github.com/Bhartendu-Kumar/DIP/blob/main/scripts/homo.py) 


5. HOMO (homo morphic filtering)
*to estimate cutoff frequency*
(*in build* : `LSSF (Large Scale Small Scale Feature Illumination Normalization` ) 

* [Histogram Distribution Functions](https://github.com/Bhartendu-Kumar/DIP/blob/main/scripts/hist_eq.py) 


6. CLAHE
*to get best clip limit*
7. HE
8. log intensity stretch
9. full scale intensity stretch
#### II. Deconvolutions / Convolutions: 


10.  [Blind Deconvolution (richardson lucy)](https://github.com/Bhartendu-Kumar/DIP/blob/main/scripts/scikit_image_algorithms.py)
(*in build* : `Blind Motion Deblurring` ) 

* [Denoising](https://github.com/Bhartendu-Kumar/DIP/blob/main/scripts/scikit_image_algorithms.py) 
11.  Total-variation denoising (tv chambolle)
*to get the best weight parameter*
(*in build* : `tv bregman` ) 
12. gaussian blur
*best sigma and kernel size*
13. bilateral filter 
estimate spatial and luminance sigmas 


 



----------------------------------------------------------------------------------------

<a id ="#Data-Sets"> </a>
### Data-Sets

----------------------------------------------------------------------------------------
#### I. Face - Data Sets:


1. BioID
2. Yale
3. MIT-CBCL
4. NMBM 
5. Caltech Face
6. Orl
7. SoF
#### II. Non-Face - Data Sets:
1. airplane  
2. car  
3. cat  
4. dog  
5. flower  
6. forest  
7. fruit  
8. motorbike
(*an illustration of dataset is in dir [data]https://github.com/Bhartendu-Kumar/DIP/tree/main/data)* : `make your data folder of same structure` ) 





 



----------------------------------------------------------------------------------------



<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Download and make the dataset folder as `data` folder in this repo. For cleaning and preprocessing. Use the scripts in the `dataset_helper_scripts` directory to convert all to greyscale and change extensions like (.gif and .pgm) to common extensions. Also arrange all images of a dataset in a single folder using these scripts.


### Installation
1. Clone the repo
   ```bash
   git clone https://github.com/Bhartendu-Kumar/DIP.git
   ```
2. Install required packages
   ```bash
   pip install -r requirements.txt
   ```
 

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

The pipeline is as:


**Step 1:** Download the DataSets (from their owner sites) and use the scripts in the dataset_helper_scripts directory to convert all to greyscale and change extensions like (.gif and .pgm) to common extensions. Also arrange all images of a dataset in a single folder using these scripts.

**Step 2:** Arrange the data   directory like shown
has 2 subdirectories: faces     non-faces
These further have their particular sub-directories with name of the DATASET


`----! Important, for illuastration "data" folder has the desired structure, just that it has few images`

**Step 3:** Run all the "driver scripts" in the root directory of this repository.
This will create an "output" directory with the result of all preprocessing methods.

**Step 4:** Use "csv_scripts" directory to get the performance metrics from the "output" directory

**Step 5:** "analysis" directory has the final performance csv files of each pre-procesing method

**Step 6:** Published report  directory has the final findings in form of csv file.


(`will update this section`).

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>






<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Bhartendu Kumar - [email](bhartendukumar1998@gmail.com) - bhartendukumar1998 	`[ @ ]`gmail` [dot]` com

Project Link: [https://github.com/Bhartendu-Kumar/DIP](https://github.com/Bhartendu-Kumar/DIP)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#top">back to top</a>)</p>







<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Bhartendu-Kumar/DIP.svg?style=for-the-badge
[contributors-url]: https://github.com/Bhartendu-Kumar/DIP/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Bhartendu-Kumar/DIP.svg?style=for-the-badge
[forks-url]: https://github.com/Bhartendu-Kumar/DIP/network/members
[stars-shield]: https://img.shields.io/github/stars/Bhartendu-Kumar/DIP.svg?style=for-the-badge
[stars-url]: https://github.com/Bhartendu-Kumar/DIP/stargazers
[issues-shield]: https://img.shields.io/github/issues/Bhartendu-Kumar/DIP.svg?style=for-the-badge
[issues-url]: https://github.com/Bhartendu-Kumar/DIP/issues
[license-shield]: https://img.shields.io/github/license/Bhartendu-Kumar/DIP.svg?style=for-the-badge
[license-url]: https://github.com/Bhartendu-Kumar/DIP/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/lena.gif
































