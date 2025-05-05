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
          description: "This is a description of the page. You can modify it in &#39;_pages/cv.md&#39;. You can also change or remove the top pdf download button.",
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
        },{id: "blogs-example-collection-part-1-getting-started",
          title: 'Example Collection: Part 1 - Getting Started',
          description: "The first part of our example blog series, laying the groundwork.",
          section: "Blogs",handler: () => {
              window.location.href = "/blogs/2024-07-27-example-collection-part1/";
            },},{id: "blogs-example-collection-part-2-more-features",
          title: 'Example Collection: Part 2 - More Features',
          description: "Exploring further capabilities in the second part of the series.",
          section: "Blogs",handler: () => {
              window.location.href = "/blogs/2024-07-28-example-collection-part2/";
            },},{id: "blogs-example-collection-part-3-wrapping-up",
          title: 'Example Collection: Part 3 - Wrapping Up',
          description: "Concluding the example series and summarizing the collection feature.",
          section: "Blogs",handler: () => {
              window.location.href = "/blogs/2024-07-29-example-collection-part3/";
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
