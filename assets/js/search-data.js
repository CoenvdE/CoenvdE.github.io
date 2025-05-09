// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "About",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-cv",
          title: "CV",
          description: "TO FIX - references, volunteer, skills, work:oceanos when done. and extra stats like grades?",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "nav-blogs",
          title: "Blogs",
          description: "I hope you find something useful here!",
          section: "Navigation",
          handler: () => {
            window.location.href = "/blogs/";
          },
        },{id: "nav-publications",
          title: "Publications",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-teaching",
          title: "Teaching",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/teaching/";
          },
        },{id: "nav-github",
          title: "Github",
          description: "My public repositories on Github.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/repositories/";
          },
        },{id: "blogs-image-paths",
          title: 'Image Paths',
          description: "",
          section: "Blogs",handler: () => {
              window.location.href = "/blogs/training-at-larger-scale/image-paths/";
            },},{id: "blogs-introduction",
          title: 'Introduction',
          description: "A comprehensive guide to scaling machine learning from small to larger training setups.",
          section: "Blogs",handler: () => {
              window.location.href = "/blogs/training-at-larger-scale/index/";
            },},{id: "blogs-the-setup",
          title: 'The Setup',
          description: "Chapter 1 of the Training at Larger Scale series",
          section: "Blogs",handler: () => {
              window.location.href = "/blogs/training-at-larger-scale/part1/";
            },},{id: "blogs-multi-gpu-training",
          title: 'Multi-GPU training',
          description: "Chapter 2 of the Training at Larger Scale series",
          section: "Blogs",handler: () => {
              window.location.href = "/blogs/training-at-larger-scale/part2/";
            },},{id: "blogs-bigger-data-in-the-cloud",
          title: 'Bigger data in the cloud',
          description: "Chapter 3 of the Training at Larger Scale series",
          section: "Blogs",handler: () => {
              window.location.href = "/blogs/training-at-larger-scale/part3/";
            },},{id: "blogs-optimizing-the-pipeline-data",
          title: 'Optimizing the pipeline: Data',
          description: "Chapter 4 of the Training at Larger Scale series",
          section: "Blogs",handler: () => {
              window.location.href = "/blogs/training-at-larger-scale/part4/";
            },},{id: "blogs-optimizing-the-pipeline-model",
          title: 'Optimizing the pipeline: Model',
          description: "Chapter 5 of the Training at Larger Scale series",
          section: "Blogs",handler: () => {
              window.location.href = "/blogs/training-at-larger-scale/part5/";
            },},{id: "blogs-what-is-next",
          title: 'What Is Next',
          description: "Chapter 6 of the Training at Larger Scale series",
          section: "Blogs",handler: () => {
              window.location.href = "/blogs/training-at-larger-scale/part6/";
            },},{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
