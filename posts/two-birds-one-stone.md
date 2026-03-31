# Two birds, one stone

*2022-09-20*

Ahh... guess I've finally got to get started and write a blog. I've been looking at things I should probably get done before I apply for a job and apparently a blog is something people like, so I've decided to kill two birds with one stone and write a blog about making a digital CV (fancy, I know).

## The idea.

I've been thinking about a few different ways I could make my digital CV, but one that I really like the thought of is having one based off of a file structure. Each heading/subheading in my CV should be a folder in this, and then each bullet point or paragraph (to be decided) will be a file, or maybe even a fancy hyperlink thingy.

That's fine, but how the hell is an somebody going to navigate this? *Well...*

![Windows 3.1 Program Manager](/static/two-birds-windows-program.png)

I really like the look of the Windows 3.1 program manager, so I think I'll use something that looks like that for navigation. Everbody loves retro too, so it'll just have to be a big hit.. right?

## Getting started

The first I'll get down to doing is defining the directory stucture and any data in it. I want this all to be in it's own seperate file so that if I, or anybody else (since I will probably decide to open-source it), wants to use this code for something else in the future they can just swap out the file for something they might want.

Since I'm going to be working in javascript I'll just chuck all the data I need into a nice big JSON file. Everybody loves JSON anyway.

```json
{
    "title": "CV",
    "structure": [
        {
            "name": "contact",
            "data": "Name: Rhys Perry\nEmail: rhysperry111@gmail.com\nWebsite: https://rhysperry.com"
        },
        {
            "name": "education",
            "structure": [
                {
                    "name": "qe",
                    "structure": [
                        {
                            "name": "alevels",
                            "data": "Computer Science\nMaths\nPhysics"
                        },
                        {
                            "name": "aslevels",
                            "data": "Economics"
                        },
                        {
                            "name": "gcses",
                            "data": "Computer Science\nMaths\nFurther Maths\nPhysics\nChemisty\nBiology\nEnglish\nGerman\nHistory"
                        }
                    ]
                }
            ]
        }
    ]
}
```

I've only added half of the CV so far, as all I need is some test data to develop the program around. I also didn't want to add too much info since this will be a publically available version so I can't include things like my address and phone number. I feel like I've also covered most of the things I'll need to test as I've got multiple levels of directories, some multi-line and some single-line files as well as a directory with more than one thing in it.

As you can see, the structure I've gone with for the file is that there is a base object with a title that I'll probably use for the program title and an array called structure that contains all the information about the directory structure. In that there can be any assortment of objects that either have a name and data (which are files), or a name and a structure array of their own (which are directories).

## Elements

Now's the time to design a few template elements that I'll use for creating the UI. I'll need five main things:

- The "desktop" will be the element that every other window lives inside. It will need:
    - To dynamically fill the whole screen
- A "window" element will be used to show a window on the screen with some contents on it. It will need:
    - A way of layering it with other windows (`position: absolute` and `z-index`?)
    - A title bar with window management buttons
    - To allow the contents to be scolled
- A "directory view" element will be used to show a list of items. It will need:
    - To automatically use the right amount of columns for the window size ([auto fill](https://developer.mozilla.org/en-US/docs/Web/CSS/repeat) looks like it will do)
- A "directory item" element to be added to the directory view. It will need:
    - A nice way to handle different length names
    - To be able to display a given icon
- A "text view" element will be used for viewing text files. It will need:
    - To... show some text

This is how I think that would would all translate into HTML:

```html
<div class="desktop-container"></div>

<div class="window-container">
    <div class="window-titlebar">
            <div class="window-close">
                <p class="window-close-text">-</p>
            </div>
            <div class="window-title">
                <p class="window-title-text"></p>
            </div>
            <div class="window-minimise">
                <p class="window-minimise-text">⌄</p>
            </div>
            <div class="window-fullscreen">
                <p class="window-fulscreen-text">⌃</p>
            </div>
    </div>
    <div class="window-content"></div>
</div>

<div class="dirview-container"></div>

<div class="diritem-container">
    <div class="diritem-icon">
        <img class="diritem-icon-image">
    </div>
    <div class="diritem-name">
        <p class="diritem-name-text"></p>
    </div>
</div>

<p class="textview-text"></p>
```

## CSSucks

Now that I have some elements to play with, I need to write up all the CSS to position things nicely and make things look fairly nice. I'll just hardcode a basic UI using the componenets above and tweak things until it looks like an actual desktop. Without the CSS it looks like it's from 2002, but unlike most developers who want to add CSS to make it look newer, I want to add CSS to make it look older... 10 years older.

```css
* {
    /* Don't know how people live without this */
    margin: 0px;
    padding: 0px;
}

.desktop-container {
    position: relative;
    width: 100%;
    height: 100%;
    background-color: grey;
}

.window-container {
    position: absolute;
    background-color: white;
    border: 2px solid black;
}

.window-titlebar {
    width: 100%;
    height: 25px;
    background-color: blue;
    color: white;
    font-weight: bold;
    display: grid;
    gap: 0px;
    grid-template-columns: 25px auto 25px 25px;
}
```

![Stuff looking already close to the Windows 3.1 style](/static/two-birds-first-css.png)

With just a littler bit of CSS it is already getting really close... which is odd given my past experiences with CSS. I might even go as far as saying I *like* working with CSS now, but something inside me says that's going too far.

![Looking almost identical to the 3.1 style](/static/two-birds-next-css.png)

I think that's all the CSS I need to do. I did end up tweaking a few things, such as changing the title bar buttons to be images rather than text, jiggled the HTML a bit, making it compliant without "quirks mode" and I also added the 3.1 tiled backgrounds, but overall it was a pretty painless experience.

## Logic

The next thing I need to work on is getting the javascript side of the code done. The basic outline of things should look something like this:

1. Load the structure metadata file
2. Create the root window
3. Listen for clicks
    - On window buttons for closing/minimising/fullscreening
    - On items in the directory view for opening another directory/opening a text viewer
    - On the titlebar to handle dragging

First I'll write some code to load the JSON file.

```js
fetch('data.json')
    .then(response => response.json())
    .then(data => {
        // Can now read the data from 'data'
    });
```

Now that I've done that, I'll need a way to create elements in javascript. I think the simplest way to do this would be to have an few classes: One for interacting with a desktop element, one base class for interacting with window elements, directory view and text view elements that will extend the window class and finally a directory item class to be added to the text views. 

My general rule for creating classes is that anything within the class that will be accessed by something else should be a direct child of the class (e.g. `myobject.name`) rather than needing to be accessed through another child (e.g. `myobject.otherchild.otherchild.name`). This does sometimes mean that I need to define setters and getters, but it keeps the code a lot cleaner outside of the class and relegates all handling of class-specific things to staying inside the class definiton.

```js
class Desktop {
    constructor(parent, width, height) {
        // Setup element
        this.element = document.createElement('div');
        this.element.className = 'desktop-container';
        this.element.style.width = width;
        this.element.style.height = height;

        // Add to parent
        parent.appendChild(this.element);
    }
}

class Window {
    constructor(desktop, width, height, title, x, y, z) {
        // Setup element
        this.element = document.createElement('div');
        this.element.className = 'window-container';
        this.element.style.width = width;
        this.element.style.height = height;
        this.element.style.left = x;
        this.element.style.top = y;
        this.element.style.zIndex = z;
        this.element.innerHTML = `
            <div class="window-titlebar">
                <div class="window-close">
                    <img class="window-close-img" src="icons/close.ico">
                </div>
                <div class="window-title">
                    <p class="window-title-text">${title}</p>
                </div>
                <div class="window-minimise">
                    <img class="window-minimise-img" src="icons/minimise.ico">
                </div>
                <div class="window-fullscreen">
                    <img class="window-fullscreen-img" src="icons/fullscreen.ico">
                </div>
            </div>
            <div class="window-content"></div>
        `;

        // Add to desktop
        desktop.element.appendChild(this.element);

        // Make content area accessible
        this.content = this.element.getElementsByClassName('window-content')[0];
    }

    get z() {
        return this.element.style.zIndex;
    }

    get width() {
        return this.element.style.width;
    }

    get height() {
        return this.element.style.height;
    }

    get x() {
        return this.element.style.left;
    }

    get y() {
        return this.element.style.top;
    }
}

class DirectoryItem {
    constructor(directoryWindow, data) {
        // Create element
        this.element = document.createElement('div');
        this.element.className = 'diritem-container';

        // Figure out item type
        let type;
        if (typeof data.data != 'undefined') {
            type = 'file';
        } else if (typeof data.structure != 'undefined') {
            type = 'folder';
        } else {
            // If unknown type, do nothing
            return;
        }

        // Set icon location based on type
        let icon;
        if (type == 'file') {
            icon = 'icons/file.ico';
        } else if (type == 'folder') {
            icon = 'icons/folder.ico';
        }

        // Add rest of HTML to element
        this.element.innerHTML = `
        <div class="diritem-icon">
            <img class="diritem-icon-image" src="${icon}">
        </div>
        <div class="diritem-name">
            <p class="diritem-name-text">${data.name}</p>
        </div>
        `;

        // Add element to directoryview
        directoryWindow.view.appendChild(this.element);
    }
}

class DirectoryWindow extends Window {
    constructor(desktop, width, height, title, x, y, z, structure) {
        // Create window
        super(desktop, width, height, title, x, y, z);

        // Create directoryview element
        this.view = document.createElement('div');
        this.view.className = 'dirview-container';

        // Add directoryview element to window
        this.content.appendChild(this.view);

        // Create items from structure
        for (let item of structure) {
            new DirectoryItem(this, item);
        }
    }
}

class TextWindow extends Window {
    constructor(desktop, width, height, title, x, y, z, data) {
        // Create window
        super(desktop, width, height, title, x, y, z);

        // Create textview element
        this.view = document.createElement('div');
        this.view.className = 'textview-container';

        // Add textview element to window
        this.content.appendChild(this.view);

        // Add text to textview
        let text = document.createElement('p');
        text.className = 'textview-text';
        text.innerText = data;
        this.view.appendChild(text);
    }
}
```

All I need to do now is add some event listeners on the directory items to spawn windows

```js
// Set click callback based on type
let callback;
if (type == 'file') {
    callback = () => {
        let x = desktop.mouseX + 'px';
        let y = desktop.mouseY + 'px';
        let z = parseFloat(directoryWindow.z) + 1;
        let width = '750px';
        let height = '500px';
        new TextWindow(desktop, width, height, data.name, x, y, z, data.data);
    };
} else if (type == 'folder') {
    callback = () => {
        let x = desktop.mouseX + 'px';
        let y = desktop.mouseY + 'px';
        let z = parseFloat(directoryWindow.z) + 1;
        let width = '600px';
        let height = '400px';
        new DirectoryWindow(desktop, width, height, data.name, x, y, z, data.structure);
    };
}

// Add callback to element
this.element.addEventListener('click', callback);
```

That was super easy, but I did need to change a few things in other places such as adding code to track the mouse position on the desktop, which then meant I had to pass the desktop through to the directory element. I'll just quickly create the main desktop and first window and see if things work

```js
fetch('data.json')
    .then(response => response.json())
    .then(data => {
        let desktop = new Desktop(document.body, '100%', '100%');
        new DirectoryWindow(desktop, '600px', '400px', data.title, '100px', '50px', 1, data.structure);
    });
```
