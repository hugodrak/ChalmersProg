from parsec import ParseError
from predicates.state import State
from predicates import guards, actions
from model.operation import Transition
from model.model import the_model

if __name__ == '__main__':
    # run in terminal when venv is sourced: python3 -m model
    try:
        model = the_model()
        print(f"The model:")
        print(f"Initial state: ")
        for k,v in model.initial_state.items():
            print(f"  {k}: {v}")
        print("")
        for name, o in model.operations.items():
            print(f"Operation {o.name}")
            print(f"  Pre: {o.precondition}")
            print(f"  Post: {o.postcondition}")
            print(f"  Effect: {o.effects}")
            print("")
        xs = [name for name, o in model.operations.items() if o.eval(model.initial_state)]
        print(f"enabled ops: {xs}")

        ## Print out more to try out your model. For example, try to do next on some enabled operations.

        # this will start the random ctrl that will run your operations in the simulator
        from runner import random_ctrl
        random_ctrl.run()
        

    except ParseError as e:
        print("The guards and actions are wrong!")
        print(f"The parser expected: {e.expected}")
        print(f"at pos {e.index} in: {e.text}")
        raise e
