# postcard-tag
Postcard Tag data export

Custom Python code to take raw data from Zooniverse and create a usable CSV that is Cortex-friendly. There are a lot of files because each workflow uses four different scripts. This may not be the most efficient way to do things, but this is the first time I've ever used Python, and it does what it needs to do.

Scripts in order:
1. p_t_data_parser
2. file_name_parser
3. merge
4. cortex_prep

- No prefix: current classify workflow as of 2023, for Monroe General and Bossier cards
- Fantastic: "Fantastic Scenes" workflow
- American: "American Scenes" workflow
- Transcribe: Transcribe Handwritten Messages

A guide to the types of Zooniverse questions and corresponding code, for help in adapting this to future worklows, is [here](https://docs.google.com/document/d/1pJ4uIKwmt7pRuLJ2i6_pYVdyEmPfQExbEFA79VpirmM/edit?usp=sharing)https://docs.google.com/document/d/1pJ4uIKwmt7pRuLJ2i6_pYVdyEmPfQExbEFA79VpirmM/edit?usp=sharing).
