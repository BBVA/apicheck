Creating a new tool
===================

Before writing new commands, check the :ref:`Commands & Tools <commands_reference>` to be sure you understand the :samp:`command` concept adequately.

What is a command?
------------------

A :samp:`command` is a small utility integrated into the ``APICheck`` suite. Usually is a **simple .py script**.

Entry point
+++++++++++

To create a new command, the only thing you need to do is create a new :samp:`.py` file with a function :samp:`main()` inside. Note that this function doesn't accept any parameters.

This function will be used as the entry point by ``APICheck``.

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

All :samp:`commands` and :samp:`tools` in ``APICheck`` can receive configuration in two ways:

- Via command line parameters.
- Via standard input (:samp:`stdin`).

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

As documented in the :ref:`Data format <data_format>` section, ``APICheck`` works internally with :samp:`JSON`. So the format received will be so.

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

To be able to chain your command into a compatible ``APICheck`` pipeline, your command must output the result of the execution to the standard output (:samp:`stdout`).
