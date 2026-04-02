%    Copyright (C) 2010  Govt. Engineering College, Thrissur
%
%	Author : Jain Basil Aliyas <jainbasil@gmail.com>
%
%    This program is free software: you can redistribute it and/or modify
%    it under the terms of the GNU General Public License as published by
%    the Free Software Foundation, either version 3 of the License, or
%    (at your option) any later version.
%
%    This program is distributed in the hope that it will be useful,
%    but WITHOUT ANY WARRANTY; without even the implied warranty of
%    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%    GNU General Public License for more details.
%Could you clarify what you need help with regarding "guru"? For example, are you asking for a definition, looking for recommendations (e.g., tech guru, spiritual guru), or something else?
%    You should have received a copy of the GNU General Public License
%    along with this program.  If not, see <http://www.gnu.org/licenses/>.

\ProvidesClass{seminar}[]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions

\LoadClass[12pt,oneside]{report}

\RequirePackage{graphicx}
\RequirePackage{float}
% The list of packages needed for creating an advanced report class.
\usepackage{caption} % in preamble (needed once)
\usepackage{algorithm}
\usepackage{longdivision}
\usepackage{multicol}
\usepackage{multirow}
\usepackage{amsmath}
\RequirePackage{fancyhdr}
\RequirePackage{amsmath}
\RequirePackage{geometry}
\RequirePackage{setspace}
\RequirePackage{titlesec}
\RequirePackage{sectsty}
\RequirePackage{times}
\usepackage{multirow}
% Macro for List of Symbols
\def\listofsymbols{\input{symbols} \clearpage}
\def\addsymbol #1: #2#3{$#1$ \> \parbox{5in}{#2 \dotfill \pageref{#3}}\\}
\def\newsymbol#1{\label{#1}} 

\renewcommand{\baselinestretch}{1.5}
\renewcommand{\bibname}{\centering {REFERENCES}}
\renewcommand*{\contentsname}{\centering{CONTENTS}}

\pagenumbering{roman}

\setcounter{secnumdepth}{5}
\setcounter{tocdepth}{5}

\usepackage{array}


\usepackage{url}
%\fancypagestyle{plain}
{
%\fancyhf{}
%\lhead{section \bfseries \thesection}
%\chead{07CS 7119 Master Research Project Phase 2, 2017}
\cfoot{ \thepage }
%\renewcommand{\headrulewidth}{0.5pt}
%\renewcommand{\footrulewidth}{0.5pt}

\newcommand{\chapfnt}{\fontsize{16}{19}}
\newcommand{\secfnt}{\fontsize{14}{17}}
\newcommand{\ssecfnt}{\fontsize{12}{14}}
\renewcommand{\chaptername}{CHAPTER}
\renewcommand{\thesection}{\arabic{section}}
\chapterfont{\centering}
\titleformat{\chapter}[display]
{\normalfont\chapfnt\bfseries\centering}{\chaptertitlename\ \thechapter}{16pt}{\chapfnt}

\titleformat{\section}
{\normalfont\secfnt\bfseries}{\thesection}{1em}{}

\titleformat{\subsection}
{\normalfont\ssecfnt\bfseries}{\thesubsection}{1em}{}

\titlespacing*{\chapter} {0pt}{1pt}{10pt}
\titlespacing*{\section} {0pt}{3.5ex plus 1ex minus .2ex}{2.3ex plus .2ex}
\titlespacing*{\subsection} {0pt}{3.25ex plus 1ex minus .2ex}{1.5ex plus .2ex}

}

%\pagestyle{fancy}
%\lhead{eries \thesection}
%\rhead{07CS 7119 Master Research Project Phase II, 2017}
%\rhead{}
%\fancyfoot{}
%\cfoot{Department of CSE, GEC, Thrissur \\ \thepage}

% for setting up alternative directory paths to graphics files,
% remember to comment in "graphics" package
%
\graphicspath{{./eps/}{./tiff/}{./jpg/}{./fig/}{./dia/}{./gnuplot/}{./png/}}

%\renewcommand{\headrulewidth}{0.5pt}
%\renewcommand{\footrulewidth}{0.5pt}
%\fancyhfoffset{10pt}
%------------
\usepackage{geometry}
\geometry{verbose,a4paper,tmargin=25.4mm,bmargin=31.75mm,lmargin=38.1mm,rmargin=31.75mm}

%To generate list of abbreviations
\usepackage{nomencl}
\makenomenclature

% setup of titlepage
%
\def\maketitle{%
\begin{titlepage}
\thispagestyle{empty}
{\centering   

{\bf{{\Large MINI PROJECT REPORT}}}\\
\vspace{10pt}
{\bf{{\Large AI-Blockchain Hybrid Phishing Defense System}}}\\

\vspace{4pt}
\makebox[\textwidth]{\textbf{Project report submitted in partial fulfillment of the Requirements for the Award of the}}\\[-10pt]
\makebox[\textwidth]{\textbf{Degree of}}
%Title must be in capital letters
%Adjust space here if the title goes to more than one line
\vspace{3pt}
\large {\textbf{BACHELOR OF TECHNOLOGY}}\\ [-5pt]
\large {\textbf{In}}\\ 

\large {\textbf{{COMPUTER SCIENCE AND ENGINEERING (AI)}}}\\ [2.5pt]
\large {\textbf{By}}\\ 

\vspace{7pt}
\large{\textbf{Akhilesh K S – SNM23CA006\\
Fresher Lonappan  – SNM23CA011\\
Navaneeth K P  – SNM23CA013\\
Soumya V B – LSNM23CA021
}}\\
\vspace{8pt}

\normalsize \textbf{Under the Guidance Of}\\
\large\textbf{ Ms. Surya T S}\\
\vspace{12pt}
\begin{figure}[ht] 
{\centering {\includegraphics[scale=.7]{Guru.PNG}}\par}
\end{figure}
\vspace{8pt}

\makebox[\textwidth]{\large\textbf{DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING}}\\
\vspace{18pt}

\makebox[\textwidth]{\large\textbf{SREE NARAYANA MANGALAM INSTITUTE OF}}\\
\makebox[\textwidth]{\large\textbf{MANAGEMENT \& TECHNOLOGY, MALIANKARA}}\\
\vspace{3pt}

\makebox[\textwidth]{\normalsize\textbf{AFFILIATED TO A P J ABDUL KALAM TECHNOLOGICAL UNIVERSITY, KERALA}}\\
\vspace{1pt}
\large{\textbf{2025-2026}}\\
}
\pagebreak
\end{titlepage}
}



