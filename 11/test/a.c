
#include "a.h"


Stack_t* createStack() {
    Stack_t *out = NULL;
    out = malloc(sizeof(Stack_t));
    if (out == NULL) {
        // exit(OUT_OF_MEMORY);
    }
    out->size = INIT_SIZE;
    out->data = malloc(out->size * sizeof(char));
    if (out->data == NULL) {
        free(out);
        // exit(OUT_OF_MEMORY);
    }
    out->top = 0;
    return out;
}
 
void deleteStack(Stack_t **stack) {
    free((*stack)->data);
    free(*stack);
    *stack = NULL;
}


void resize(Stack_t *stack) {
    stack->size += ADD_SIZE;
    stack->data = realloc(stack->data, stack->size * sizeof(char));
    if (stack->data == NULL) {
        // exit(STACK_OVERFLOW);
    }
}

void push(Stack_t *stack, char value) {
    if (stack->top >= stack->size) {
        resize(stack);
    }
    stack->data[stack->top] = value;
    stack->top++;
}


char pop(Stack_t *stack) {
    if (stack->top == 0) {
        // exit(STACK_UNDERFLOW);
    }
    stack->top--;
    return stack->data[stack->top];
}
char peek(const Stack_t *stack) {
    if (stack->top <= 0) {
        // exit(STACK_UNDERFLOW);
    }
    return stack->data[stack->top - 1];
}

//=======================================



Stack_f* createFStack() {
    Stack_f *out = NULL;
    out = malloc(sizeof(Stack_f));
    if (out == NULL) {
        // exit(OUT_OF_MEMORY);
    }
    out->size = INIT_SIZE;
    out->data = malloc(out->size * sizeof(double));
    if (out->data == NULL) {
        free(out);
        // exit(OUT_OF_MEMORY);
    }
    out->top = 0;
    return out;
}
 
void deleteFStack(Stack_f **stack) {
    free((*stack)->data);
    free(*stack);
    *stack = NULL;
}


void Fresize(Stack_f *stack) {
    stack->size += ADD_SIZE;
    stack->data = realloc(stack->data, stack->size * sizeof(double));
    if (stack->data == NULL) {
        // exit(STACK_OVERFLOW);
    }
}

void Fpush(Stack_f *stack, double value) {
    if (stack->top >= stack->size) {
        Fresize(stack);
    }
    stack->data[stack->top] = value;
    stack->top++;
}


double Fpop(Stack_f *stack) {
    if (stack->top == 0) {
        // exit(STACK_UNDERFLOW);
    }
    stack->top--;
    return stack->data[stack->top];
}
double Fpeek(const Stack_f *stack) {
    if (stack->top <= 0) {
        // exit(STACK_UNDERFLOW);
    }
    return stack->data[stack->top - 1];
}

