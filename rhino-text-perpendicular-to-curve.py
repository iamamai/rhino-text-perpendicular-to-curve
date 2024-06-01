import Rhino
from scriptcontext import doc

members = []

# Define the prompt message
prompt = "List of items separated by a comma. Use double hyphens (--) instead of spaces in each item, e.g., Make--instant--noodles,Brew--filter--coffee,woodblock-print,editor-in-chief"

# Function to get user input using Rhino's GetString method
def get_user_input(prompt):
    gs = Rhino.Input.Custom.GetString()
    gs.SetCommandPrompt(prompt)
    if gs.Get() == Rhino.Input.GetResult.String:
        return gs.StringResult()
    return None

# Prompt the user to input the list
user_input = get_user_input(prompt)

# Check if the user provided input and didn't cancel
if user_input:
    # Split the user input by "," to form the members list
    members = [item.strip().replace("--", " ") for item in user_input.split(",")]

# Input curve
crv = Rhino.Input.RhinoGet.GetOneObject("Pick a curve", False, Rhino.DocObjects.ObjectType.Curve)[1].Curve()

# Generate planes for the perpendicular text and text attributes
planes = crv.GetPerpendicularFrames(crv.DivideByCount(len(members)-1, True))
for text,plane in zip(members,planes):
    entity = Rhino.Geometry.TextEntity()
    entity.Text = text
    entity.Plane = Rhino.Geometry.Plane(plane.Origin, -plane.XAxis, -plane.ZAxis)
    entity.Justification = Rhino.Geometry.TextJustification.Left
    entity.DrawForward = False
    entity.FontIndex = doc.Fonts.FindOrCreate("Arial", False, False)
    doc.Objects.AddText(entity)
    doc.Views.Redraw()