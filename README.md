# Proposals
My ideas for my final project are...

1.  Use web scraping (**requests**, **beautifulsoup**) to get the organization charts off of .gov websites and use image recognition (ChatGPT?) and a nested dictionary and/or **igraph** to map the entire government structure of Illinois (with the intention of later replicating to every state and the federal government). I've looked into it and it doesn't look like such a comprehensive graph exists.
2. A manifesto for the replacement of some types of journal articles, such as literature reviews, with the purpose of de-emphasizing individual studies in favor of reviews and the end goal of mitigating replication crises. **Case study: most effective policies to increase student achievement**
   1. Most of the time, quality literature reviews on a certain topic rely on the initiative of individuals to conduct a broad overview of their field. Even these can be relatively indigestible, to researchers but also to the broader public. Medium has the correct level of accessibility, but is less good in terms of rigor and credibility. Journals have the reverse problem. Additionally, one of the greater problems in online educational/expository resources is lack of ability to adapt to the audience level, in the way that an individual mentor could. That sense of powerlessness one gets at being told to “search the internet” to find out about a topic…Is it just AI-powered searching that we need? Or a complete rethinking of the way we organize reference content on the web?
   2. Specifications
      1. open source - live document that is updated frequently by many experts (GitHub Pages)
      2. readers/users can leave feedback directly on the project (how to quality control?)
      3. accessible - language is analyzed for legibility to non-expert audiences (`py-readability-metrics`). 
      4. multimodal - includes images, diagrams, videos, and other graphical elements to explain a process visually. *possibly also embedded interactive exercises/examples. the less words, the better (except for the purpose of web accessibility)
      5. reproducible - describes methods for meta-analysis that can be applied repeatedly and systematically as new information comes out
      6. efficient data centralization - instead of several different meta-analyses by individual groups, the *same article will be updated at the same web address over time*, with different sections describing different approaches as needed
      7. trustworthy - retain the credibility of journals, eg by requiring peer review of each new article/edition (via branches/GitHub)
      8. change log - can view version history over time. do not overwrite past editions, despite updating (GitHub)
      9. narrative and/or standardized organization - one nice thing about journal articles currently is that you know what to expect and where to find certain types of information. narrative structure, with examples, is important for comprehension and retention???? 
      10. audience adaptability - show or hide sections or label on a "need-to-know" basis
          1. left panel with outline hyperlinks for center panel: BEGINNER, INTERMEDIATE, EXPERT levels of explanation???? some innovative way of linking articles possibly link related individual studies with high h factor (maybe knowledge graph ...?) 
          2. right panel - temporarily open related articles could be summary versions? similar to wikipediaor maybe right panel can be more detailed expansion of whatever’s on the left

   3.  Every month, get the top 10 newest, most cited papers in student achievement from **OpenAlex API**. Using **pypdf2**, read in files and using **re** or LLM API, find the main variables, methods, populations, findings of the paper. (Try the Cochrane meta analysis standards as a guide.) Ideally, these would sit in a repository until a human is able to review these (human in the loop design). 
   4. Or, assuming, you already have a meta-analysis, focus on editing and presenting it for public consumption. Summarize on 3 levels using **LLM API**. Create a web app including visualizations using **pandas** and **streamlit**.


3. Use web scraping (?) (**requests**, **beautifulsoup**) to get video recordings of Chicago city council meetings (could assume we already have video files if this is too ambitious), use **Whisper** to transcribe the video (may need an intermediate step to divorce audio file from video file), use **LLM (Otter?) API** to summarize the notes, generate a poll of major decision points (how?), and send the poll as an automated email where a subscribed citizen can send in their approval or disapproval of each meeting.

## To-do list

**Goal: dashboard to help with meta-analyses + platform to host the finished product**

| Task                                                         | Week due | Progress      | Notes                     |
| ------------------------------------------------------------ | -------- | ------------- | ------------------------- |
| Setup environments, look into LLM packages                   | 4        | Done          | No viable free LLMs found |
| Figure out `streamlit` and get minimal working page          | 5        | Working on it |                           |
| Connect to `openalex` and filter for new papers in topic of interest. Output to folder for human review | 6        |               |                           |
| Attempt to summarize papers (extract methods, population, etc. using [`spacy` or `gensim`](https://www.turing.com/kb/5-powerful-text-summarization-techniques-in-python)) | 7        |               |                           |
| Research how to do Cochrane meta-analysis and summarize any relevant statistics (eg, categorize as significant or non-significant) | 8        |               |                           |
| Get 3-column layout in Streamlit. Add visualizations of the meta-analysis results with `matplotlib` | 9        |               |                           |
| Add readability checker with [`py-readability-metrics`](https://levelup.gitconnected.com/determine-the-reading-level-of-a-text-with-python-d2f9dccee6bf) | 10       |               |                           |
