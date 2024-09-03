
import gradio as gr
from gradio_sequence_editor import sequence_editor


with gr.Blocks(css=".form { overflow: visible } .sequence_editor { overflow: visible !important; }") as demo:
    sequence = sequence_editor(sequences="ABCDE", width=360, editor_visible=False, elem_classes=['sequence_editor'])
    print_btn = gr.Button('Print')
    def update_sequence():
        return sequence_editor(sequences=""">target
PPKPFFFEAGERAVLLLHGFTGNSADVRMLGRFLESKGY----------GVPPEELVHTG
PDDWWQDVMNGYEFLKNKGYEKIAVAGLSLGGVFSLKLGYTVPIEGIVTMCAPMYIKSEE
TMYEGVLEYAREYKKREGKSEEQIEQEMEKFKQTPMKTLKALQELIADVRDHLDLIYAPT
FVVQARHDEMINPDSANIIYNEIESPVKQIKWYEQSGHVITLDQEKDQLHEDIYAFLESL
DW
>template
PPKPFFFEAGERAVLLLHGFTGNSADVRMLGRFLESKGYTCHAPIYKGHGVPPEELVHTG
PDDWWQDVMNGYEFLKNKGYEKIAVAGLSLGGVFSLKLGYTVPIEGIVTMCAPMYIKSEE
TMYEGVLEYAREYKKREGKSEEQIEQEMEKFKQTPMKTLKALQELIADVRDHLDLIYAPT
FVVQARHDEMINPDSANIIYNEIESPVKQIKWYEQSGHVITLDQEKDQLHEDIYAFLESL
DW""", width=720, toolbar_visible=False)
    print_btn.click(update_sequence, outputs=sequence)

if __name__ == "__main__":
    demo.launch()
