Creating a new commands
=======================

Before start writing new commands check the :ref:`Command & tools <commands_reference>` to be sure you understand the :samp:`command` concept properly.

What is a command?
------------------

A :samp:`command` is a small utility integrated into the ``APICheck`` suite. Usually is a **simple .py script**.

Entry point
+++++++++++

To create a new command the only thing you need to do is create a new :samp:`.py` file with the function :samp:`main()` inside. This function doesn't receive any parameters.

This function will be used as entry point for ``APICheck``.

.. code-block:: python
   :linenos:
   :emphasize-lines: 6
   :caption: my_command.py

    import argparse

    #
    # This function is the COMMAND entry point
    #
    def main():
      #
      # YOUR CODE HERE
      #
      print("My new command!")

    if __name__ == '__main__':
        main()


**Passing information along**

All :samp:`commands` and :samp:`tools` in ``APICheck`` can receive configuration by to ways:

- By command line parameters.
- By standard input (:samp:`stdin`).

This means that your command must be able to be executed as part of a *pipeline*.

.. code-block:: python
   :linenos:
   :emphasize-lines: 9-13
   :caption: my_command.py

    import sys
    import argparse

    def main():

      #
      # Read from STDIN or cli ARGS
      #
      if len(sys.argv) > 0:
        with open(sys.argv[0], "r") as f:
            input_content = f.read()
      else:
        input_content = sys.stdin.read()

      print("Input content: ", input_content)

    if __name__ == '__main__':
        main()

**Data format**

As documented in the section :ref:`Data format <data_format>`, ``APICheck`` works internally with :samp:`JSON`. So the format received will be so.

Following the previous example, we add parsing JSON format:

.. code-block:: python
   :linenos:
   :emphasize-lines: 16-20
   :caption: my_command.py

    import sys
    import json
    import argparse

    def main():

      if len(sys.argv) > 0:
        with open(sys.argv[0], "r") as f:
            input_content = f.read()
      else:
        input_content = sys.stdin.read()

      #
      # Parsed
      #
      try:
         formatted_json = json.loads(input_content)
      except json.decoder.JSONDecodeError:
         print("[!] Invalid JSON input format")
         exit(1)

      print("Input content: ", formatted_json)

    if __name__ == '__main__':
        main()


Output information
++++++++++++++++++

To be able to chain your command into a compatible ``APICheck`` pipeline, your command must output the execution result to the standard output (:samp:`stdout`).
