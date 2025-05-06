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
          description: "TO FIX - references, volunteer, skills, work.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "nav-blogs",
          title: "Blogs",
          description: "Explore my different blog collections",
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
        },{id: "blogs-dummy-collection",
          title: 'Dummy Collection',
          description: "A placeholder collection to demonstrate multiple blog series.",
          section: "Blogs",handler: () => {
              window.location.href = "/blogs/dummy/index/";
            },},{id: "blogs-part-1-getting-started",
          title: 'Part 1 - Getting Started',
          description: "The first part of our example blog series, laying the groundwork.",
          section: "Blogs",handler: () => {
              window.location.href = "/blogs/example-collection/part1/";
            },},{id: "blogs-part-2-more-features",
          title: 'Part 2 - More Features',
          description: "Exploring further capabilities in the second part of the series.",
          section: "Blogs",handler: () => {
              window.location.href = "/blogs/example-collection/part2/";
            },},{id: "blogs-part-3-wrapping-up",
          title: 'Part 3 - Wrapping Up',
          description: "Concluding the example series and summarizing the collection feature.",
          section: "Blogs",handler: () => {
              window.location.href = "/blogs/example-collection/part3/";
            },},{id: "blogs-dummy-post-part-1",
          title: 'Dummy Post - Part 1',
          description: "The first and only part of the dummy collection.",
          section: "Blogs",handler: () => {
              window.location.href = "/blogs/dummy/part1/";
            },},{id: "blogs-example-collection-a-series",
          title: 'Example Collection: A Series',
          description: "An example blog series showing the folder-based structure with a landing page.",
          section: "Blogs",handler: () => {
              window.location.href = "/blogs/example-collection/index/";
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
