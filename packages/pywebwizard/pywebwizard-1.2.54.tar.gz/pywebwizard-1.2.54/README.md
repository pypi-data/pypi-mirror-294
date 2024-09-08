# PyWebWizard: Browser Automation

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [Setup](#setup)
- [Usage](#usage)
  * [Web Elements: Interfaces](#web-elements-interfaces)
  * [Actions with Examples](#actions-with-examples)
  * [Loop Actions and Their Modes](#loop-actions-and-their-modes)
  * [Timeout for Element Selection](#timeout-for-element-selection)
  * [Browser Configuration](#browser-options)
- [Contributions](#contributions)
- [License](#license)

## Description

WebWizard is an automation tool that uses Selenium to perform various actions in the browser. Designed with flexibility in mind, WebWizard is driven by a YAML configuration, allowing users to navigate websites, interact with elements, capture screenshots, and much more.

## Features

- **Navigation:** Seamlessly navigate to any provided URL.
- **Interaction:** Fill fields, click on elements, scroll through pages, and simulate keyboard inputs.
- **Screenshot:** Capture the current web page with options to modify element styles before capturing.
- **Loops:** Introduce automation loops either through defined times, local files, or even URLs.
- **Configurable:** Easily customizable through a `config.yaml` file.

## Requirements

- Python 3.x
- Python Packages: `selenium`, `yaml`

## Configuration

WebWizard's heart lies in its `config.yaml` file. This configuration file allows you to define various actions (`start`) and some additional settings (`config`).


## Setup

1. Clone or download the repository.
2. Install the required dependencies with `python3 pip install -r requirements.txt`.
3. Modify the `config.yaml` file following the structure and examples provided.
4. Execute the main script: `python main.py`.

## Usage

### In a Python script
```python
from pywebwizard.utils.config import BROWSER_OPTIONS, INTERFACES, METHODS
from pywebwizard import PyWebWizard
```


### In the command-line
```shell

```

## Web Elements: Interfaces

In WebWizard, interfaces play a crucial role in identifying and interacting with web elements. They provide a way to pinpoint specific elements on a web page. Here are the available interfaces with brief explanations and examples for each:

### 1. `id`

The `id` interface targets elements based on their unique `id` attribute.

```yaml
elements:
  name_field:
    interface: id
    query: name_id
```

### 2. `name`

The `name` interface focuses on elements using their `name` attribute, often used in form fields.

```yaml
elements:
  email_field:
    interface: name
    query: email_name
```

### 3. `xpath`

The `xpath` interface allows for powerful and flexible navigation of the HTML structure.

```yaml
elements:
  message_box:
    interface: xpath
    query: //div/textarea[@name="message"]
```

### 4. `css`

The `css` interface uses CSS selectors to identify elements.

```yaml
elements:
  submit_button:
    interface: css
    query: .submit-btn-class
```

### 5. `class`

The `class` interface locates elements based on their class attribute.

```yaml
elements:
  notification:
    interface: class
    query: notification-class
```

### 6. `tag`

The `tag` interface finds elements based on their HTML tag name.

```yaml
elements:
  all_images:
    interface: tag
    query: img
```

### 7. `link_text`

The `link_text` interface targets anchor tags (`<a>`) using the exact text they display.

```yaml
elements:
  signup_link:
    interface: link_text
    query: Sign Up Now!
```

### 8. `link_text_partial`

The `link_text_partial` interface is similar to `link_text` but matches based on a part of the anchor tag's text.

```yaml
elements:
  partial_link:
    interface: link_text_partial
    query: Sign
```

Each of these interfaces offers a different way to interact with web elements. The choice of interface largely depends on the specific requirements of your automation tasks and the structure of the web page you're working with.

### Actions with Examples

Below are the actions available and a brief example for each:

- **Navigate:** Directs the browser to a specific URL.
  ```yaml
  - action: navigate
    url: https://example.com/
  ```
  
- **Loop:** Automate repetitive tasks using loops. You can loop a fixed number of times, or iterate over local/remote JSON files.
  ```yaml
  - action: loop
    times: 5
    do:
      - action: fill
        interface: id
        query: email
        content: example@email.com
  ```

- **Fill:** Populate fields on the webpage.
  ```yaml
  - action: fill
    <<: *name_field
    content: John Doe
  ```
  
- **Keyboard:** Simulate keyboard presses like 'tab', 'enter', etc. This action keys are the combination on keyboard keys. All keys added to this list are going to be pressed at the same time.
  ```yaml
  - action: keyboard
    keys:
      - "tab"
  ```
  
- **Scroll:** Scroll in the active website tab on x or y axis. At least one of x or y value need to be set.
  ```yaml
  - action: scroll
    x: 0
    y: 200
  ```
  
- **Execute JS:** Execute JavaScript commands in the browser.
  ```yaml
  - action: execute
    js: "$('#name').addClass('example')"
  ```
  
- **Wait for element:** Waits for an element to exist a maximum of time. Default 10 seconds.
  ```yaml
  - action: wait
    interface: id
    query: name
    timeout: 10
  ```
  
- **Screenshot:** Capture the webpage. You can also apply CSS before taking the screenshot like in this example referencing an element by the interface and query and set literally the style you give.
  ```yaml
  - action: screenshot
    file_name: capture
    css:
      - interface: id
        query: email_field
        style: "border: 3px solid blue;"
  ```

## Loop Actions and Their Modes

The `loop` action in WebWizard allows users to automate repetitive tasks. There are three modes available for looping:

### 1. `times`

Iterate a set of actions for a specified number of times. This is useful for performing a repetitive task without the need for external data.

```yaml
- action: loop
  times: 5
  do:
    - action: fill
      interface: id
      query: email
      content: example@email.com
```

### 2. `source` (Local JSON File)

Use a local JSON file as a source for looping. Each entry in the JSON file can be used for each iteration. The `do__key` format allows you to pull data from the JSON's keys for each iteration.

```yaml
- action: loop
  source: F:\PARENDUM\Software\autobrowser\data.json
  do:
    - action: fill
      interface: id
      query: name_field
      content: do__name
```

### 3. `source` (URL)

Similar to the local JSON file mode, but this time the source is a remote URL which returns a JSON. The same `do__key` format applies here.

```yaml
- action: loop
  source: http://example.com/data.json
  do:
    - action: fill
      interface: id
      query: name_field
      content: do__name
```

### 3. `raw` (URL)

This raw could be a JSON string. The same `do__key` format applies here.

```yaml
- action: loop
  raw: "{'name': 'Kevin'}"
  do:
    - action: fill
      interface: id
      query: name_field
      content: do__name
```

Using the `do__key` format, you can dynamically pull data from your JSON (whether local or from a URL) and use it in your actions. This provides a powerful way to automate tasks with varying data.

### Timeout for Element Selection

In scenarios where WebWizard tries to interact with an element that may not be immediately available, a `timeout` feature is available to avoid abrupt errors or exceptions. By default, WebWizard will wait for up to 10 seconds for an element to become available before throwing an exception. This is particularly useful in situations where the webpage might take some time to load all its elements, especially in cases of heavy JavaScript usage or slow network speeds.

You can specify the `timeout` parameter alongside the `interface` and `query` in your element selection configuration. Here's how you can do it:

```yaml
elements:
  dynamic_content:
    interface: id
    query: name
    timeout: 15  # Wait up to 15 seconds for the element
```

In the example above, WebWizard waits for up to 15 seconds for an element with the specified ID to appear. If the element doesn't become available within this time, an exception will be thrown, and you'll be informed of the timeout incident, allowing you to handle these cases gracefully in your automation script.

Remember, while the default wait time is 10 seconds, you can adjust the `timeout` to any number of seconds that suits your needs, depending on the expected behavior of the web pages you are interacting with.



### Browser Configuratioin

Choose from supported browsers:
```yaml
config: 
  - browser: firefox  # firefox, chrome, ...
```

Choose hidden or not:
```yaml
config: 
  - hidden: true
```

Choose destroy or not web browser when finishing:
```yaml
config: 
  - destroy: true
```

Choose screenshots directory:
```yaml
config: 
  - screenshots: C:\images
```

(Optional) Your remote selenium docker image URL:
```yaml
config: 
  - remote: https://my-remote-instance.company.com/
```

## Contributions

Your contributions enrich the WebWizard community! Whether it's a bug report, feature suggestion, or a code contribution, all are appreciated. For contributions, please submit a Pull Request.

## License

WebWizard is licensed under the MIT License. For a comprehensive understanding, refer to the LICENSE file.
