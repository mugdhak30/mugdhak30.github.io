---
layout: archive
title: ""
permalink: /teaching/
author_profile: true
---

**Teaching Assistance**
======

* [Seminar Secure Systems Engineering](https://www.hni.uni-paderborn.de/sse/lehre/seminar-secure-systems-engineering-ss-2023/) \\
Master Course, Universität Paderborn (Summer 2023)\\
This course offers a unique opportunity for students to understand and experience how scientific research is conducted.

* [Designing Code Analyses for Large-scale Software Systems I](https://www.hni.uni-paderborn.de/sse/lehre/deca/) \\
Master Course, Universität Paderborn (Winter 2022, Winter 2021)\\
This course covers several concepts in static code analysis: intra-procedural data-flow analysis, call-graph construction algorithms, context-insensitivity, pointer analysis, analysis frameworks (IFDS, IDE, VASCO).

* [Designing Code Analyses for Large-scale Software Systems II](https://www.hni.uni-paderborn.de/sse/lehre/designing-code-analyses-for-large-scale-software-systems-2-deca-2-ss2022/)\\
  Master Course, Universität Paderborn (Summer 2022, Summer 2021)\\
This course covers several novel, advanced concepts in static code analysis: sparse IFDS, pushdown systems, demand-driven program analysis, hybrid analysis and improved user experience.

**Supervision**
=====
I have supervised the following Master or Seminar theses:
* Master thesis - Improving User Experience of Program Slicing wrt Data Privacy (ongoing)
* Master thesis - Labeling User-Input Privacy Data in Android Applications (ongoing)
* Master thesis - Empirical Evaluation of Forward and Backward Taint Analysis (finished)
* Master thesis - Qualitative Study of Data Flow Analysis Frameworks: IFDS, IDE and VASCO (finished)
* [Seminar Secure Systems Engineering (Summer 2023)](https://www.hni.uni-paderborn.de/sse/lehre/seminar-secure-systems-engineering-ss-2023/) - Machine Learning-Based Identification of Personal Data Sources in Android (finished)
* [Seminar Secure Systems Engineering (Summer 2023)](https://www.hni.uni-paderborn.de/sse/lehre/seminar-secure-systems-engineering-ss-2023/) - Loopholes in Google Play’s Data Safety Section (finished)
[Seminar Secure Systems Engineering (Winter 2022)](https://www.hni.uni-paderborn.de/sse/lehre/seminar-secure-systems-engineering-ws-20222023/) - Studying Pseudonymisation Techniques for Data Protection (finished)
* [Seminar Secure Systems Engineering (Summer 2022)](https://www.hni.uni-paderborn.de/sse/lehre/seminar-secure-systems-engineering-ss-2022/) - A Survey of Compliance Standards (finished)
* [Seminar Secure Systems Engineering (Winter 2021)](https://www.hni.uni-paderborn.de/sse/lehre/vorlesungsarchiv/ws-202122/seminar-secure-systems-engineering-ws-2021/) - A Survey of Parametric Static Analysis (finished)

For students seeking a thesis topic, organizational information [on my webpage](https://mugdhak30.github.io/info_for_students/) and on the [SSE webpage](https://www.hni.uni-paderborn.de/sse/lehre/bachelor-masterarbeiten/) might interest you. 

{% include base_path %}

{% for post in site.teaching reversed %}
  {% include archive-single.html %}
{% endfor %}
